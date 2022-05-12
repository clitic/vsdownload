import re
import statistics
import urllib.parse
from typing import Union, Optional, Tuple
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES


def find_absolute_uri(baseurl: Union[str, None], m3u8_data) -> str:
    """finds absolute uri to the given m3u8 data

    Args:
        baseurl (str): baseurl to use
        m3u8_data: any object from m3u8 library

    Returns:
        str: absolute uri
    """
    if baseurl is None:
        return m3u8_data.absolute_uri
    elif not m3u8_data.uri.startswith("http"):
        return urllib.parse.urljoin(baseurl, m3u8_data.uri)
    else:
        return m3u8_data.uri
        
def decrypt_aes_data(cipher_data: bytes, key: bytes, iv: Union[str, None]) -> bytes:
    """decrypts standard aes cbc encrypted data

    Args:
        cipher_data (bytes): bytes data of file
        key (bytes): encryption key
        iv (Union[str, None]): encryption iv

    Returns:
        bytes: decrypted bytes data
    """
    cipher_data = pad(data_to_pad=cipher_data, block_size=AES.block_size)
    return AES.new(key=key, mode=AES.MODE_CBC, IV=iv).decrypt(cipher_data)

def convertbytes(bytesval: Union[int, float]) -> Tuple[str, Union[int, float], str]:
    """convert bytes value to string representation

    Args:
        bytesval (Union[int, float]): value

    Returns:
        Tuple[str, Union[int, float], str]: tuple containing formatted bytes string
    """
    for unit in ["bytes", "KB", "MB", "GB", "TB"]:
        if bytesval < 1024.0:
            return ("{:.2f} {}".format(bytesval, unit), bytesval, unit)
        bytesval /= 1024.0
        
def find_urls_by_ext(text: str, ext: str, commanurls: Optional[bool] = True) -> list:
    """find urls with specific extension from a text string using regular expressions

    Args:
        text (str): text to search for
        ext (str): extension to use
        commanurls (Optional[bool], optional): sort out unique urls only. Defaults to True.

    Returns:
        list: list of urls found
    """
    regex = re.compile(rf"(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-]\.{ext})")
    # regex = re.compile(rf"https?://[a-zA-Z0-9-._%/]*\.{ext}")
    matches = re.findall(regex, text)
    matches = map(lambda x: f"{x[0]}://{x[1]}{x[2]}", matches)

    if commanurls:
        return list(matches)

    urls = []
    for match in matches:
        if match not in urls:
            urls.append(match)

    return urls

def find_baseurl_by_urls(listofurls: list, ext: str, static: Optional[bool] = True) -> Union[str, None]:
    """find out most possible baseurl from bunch of urls using regular expressions

    Args:
        listofurls (list): list of urls
        ext (str): extension to use
        static (Optional[bool], optional): returns statistics mode of possible baseurl instead of first baseurl. Defaults to True.

    Returns:
        Union[str, None]: most possible baseurl
    """
    regex = re.compile(rf"[^/][a-zA-Z0-9-._%]*\.{ext}")

    possible_base_urls = []
    for link in listofurls:
        matches = re.findall(regex, link)
        for match in matches:
            possible_base_urls.append(link.split(match)[0])

    try:
        if static:
            return statistics.mode(possible_base_urls)
        else:
            return possible_base_urls[0]
    except:
        return None
