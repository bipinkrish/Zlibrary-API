import requests
from typing import Union, Dict

class Zlibrary:

    def __init__(self, email: str = None, password: str = None, remix_userid: Union[int, str] = None, remix_userkey: str = None):
        self.__email: str
        self.__name: str
        self.__kindle_email: str
        self.__remix_userid: Union[int, str]
        self.__remix_userkey: str
        self.__domain = "https://singlelogin.se"
        self.__downloadDomains = ["zlibrary-in.se", "zlibrary-africa.se"]
        self.__logged = False

        self.__headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        }
        self.__cookies = {
            "siteLanguageV2": "en",
        }

        if email is not None and password is not None:
            self.login(email, password)
        elif remix_userid is not None and remix_userkey is not None:
            self.loginWithToken(remix_userid, remix_userkey)

    def __setValues(self, response) -> Dict[str, str]:
        if not response["success"]:
            return response
        self.__email = response["user"]["email"]
        self.__name = response["user"]["name"]
        self.__kindle_email = response["user"]["kindle_email"]
        self.__remix_userid = str(response["user"]["id"])
        self.__remix_userkey = response["user"]["remix_userkey"]
        self.__cookies["remix_userid"] = self.__remix_userid
        self.__cookies["remix_userkey"] = self.__remix_userkey
        self.__logged = True
        return response

    def __login(self, email, password) -> Dict[str, str]:
        return self.__setValues(self.__makePostRequest('/eapi/user/login', data={
            "email": email,
            "password": password,
        }, override=True))

    def __checkIDandKey(self, remix_userid, remix_userkey) -> Dict[str, str]:
        return self.__setValues(self.__makeGetRequest('/eapi/user/profile', cookies={
            'siteLanguageV2': 'en',
            'remix_userid': str(remix_userid),
            'remix_userkey': remix_userkey,
        },))

    def login(self, email: str, password: str) -> Dict[str, str]:
        return self.__login(email, password)

    def loginWithToken(self, remix_userid: Union[int, str], remix_userkey: str) -> Dict[str, str]:
        return self.__checkIDandKey(remix_userid, remix_userkey)

    def __makePostRequest(self, url: str, data: dict = {}, override=False) -> Dict[str, str]:
        if not self.__logged and override is False:
            print("Not logged in")
            return
        response = requests.post(
            self.__domain + url,
            data=data,
            cookies=self.__cookies,
            headers=self.__headers,
        ).json()
        if not response["success"]:
            print(response["error"])
        return response

    def __makeGetRequest(self, url: str, params: dict = {}, cookies=None) -> Dict[str, str]:
        if not self.__logged and cookies is None:
            print("Not logged in")
            return
        response = requests.get(
            self.__domain + url,
            params=params,
            cookies=self.__cookies if cookies is None else cookies,
            headers=self.__headers,
        ).json()
        if not response["success"]:
            print(response["error"])
        return response

    def getProfile(self) -> Dict[str, str]:
        return self.__makeGetRequest('/eapi/user/profile')

    def getMostPopular(self, switch_language: str = None) -> Dict[str, str]:
        if switch_language is not None:
            return self.__makeGetRequest('/eapi/book/most-popular', {"switch-language": switch_language})
        return self.__makeGetRequest('/eapi/book/most-popular')

    def getRecently(self) -> Dict[str, str]:
        return self.__makeGetRequest('/eapi/book/recently')

    def getUserRecommended(self) -> Dict[str, str]:
        return self.__makeGetRequest('/eapi/user/book/recommended')

    def deleteUserBook(self, bookid: Union[int, str]) -> Dict[str, str]:
        return self.__makeGetRequest(f'/eapi/user/book/{bookid}/delete')

    def unsaveUserBook(self, bookid: Union[int, str]) -> Dict[str, str]:
        return self.__makeGetRequest(f'/eapi/user/book/{bookid}/unsave')

    def getBookForamt(self, bookid: Union[int, str], hashid: str) -> Dict[str, str]:
        return self.__makeGetRequest(f'/eapi/book/{bookid}/{hashid}/formats')

    def getDonations(self) -> Dict[str, str]:
        return self.__makeGetRequest('/eapi/user/donations')

    def getUserDownloaded(self, order: str = None, page: int = None, limit: int = None) -> Dict[str, str]:
        '''
        order takes one of the values\n
        ["year",...]
        '''
        params = {k: v for k, v in {"order": order, "page": page,
                                    "limit": limit}.items() if v is not None}
        return self.__makeGetRequest('/eapi/user/book/downloaded', params)

    def getExtensions(self) -> Dict[str, str]:
        return self.__makeGetRequest('/eapi/info/extensions')

    def getDomains(self) -> Dict[str, str]:
        return self.__makeGetRequest('/eapi/info/domains')

    def getLanguages(self) -> Dict[str, str]:
        return self.__makeGetRequest('/eapi/info/languages')

    def getPlans(self, switch_language: str = None) -> Dict[str, str]:
        if switch_language is not None:
            return self.__makeGetRequest('/eapi/info/plans', {"switch-language": switch_language})
        return self.__makeGetRequest('/eapi/info/plans')

    def getUserSaved(self, order: str = None, page: int = None, limit: int = None) -> Dict[str, str]:
        '''
        order takes one of the values\n
        ["year",...]
        '''
        params = {k: v for k, v in {"order": order, "page": page,
                                    "limit": limit}.items() if v is not None}
        return self.__makeGetRequest('/eapi/user/book/saved', params)

    def getInfo(self, switch_language: str = None) -> Dict[str, str]:
        if switch_language is not None:
            return self.__makeGetRequest('/eapi/info', {"switch-language": switch_language})
        return self.__makeGetRequest('/eapi/info')

    def hideBanner(self) -> Dict[str, str]:
        return self.__makeGetRequest('/eapi/user/hide-banner')

    def recoverPassword(self, email: str) -> Dict[str, str]:
        return self.__makePostRequest('/eapi/user/password-recovery', {"email": email}, override=True)

    def makeRegistration(self, email: str, password: str, name: str) -> Dict[str, str]:
        return self.__makePostRequest('/eapi/user/registration', {"email": email, "password": password, "name": name}, override=True)

    def resendConfirmation(self) -> Dict[str, str]:
        return self.__makePostRequest('/eapi/user/email/confirmation/resend')

    def saveBook(self, bookid: Union[int, str]) -> Dict[str, str]:
        return self.__makeGetRequest(f'/eapi/user/book/{bookid}/save')

    def sendTo(self, bookid: Union[int, str], hashid: str, totype: str) -> Dict[str, str]:
        return self.__makeGetRequest(f'/eapi/book/{bookid}/{hashid}/send-to-{totype}')

    def getBookInfo(self, bookid: Union[int, str], hashid: str, switch_language: str = None) -> Dict[str, str]:
        if switch_language is not None:
            return self.__makeGetRequest(f'/eapi/book/{bookid}/{hashid}', {"switch-language": switch_language})
        return self.__makeGetRequest(f'/eapi/book/{bookid}/{hashid}')

    def getSimilar(self, bookid: Union[int, str], hashid: str) -> Dict[str, str]:
        return self.__makeGetRequest(f'/eapi/book/{bookid}/{hashid}/similar')

    def makeTokenSigin(self, name: str, id_token: str) -> Dict[str, str]:
        return self.__makePostRequest('/eapi/user/token-sign-in', {"name": name, "id_token": id_token}, override=True)

    def updateInfo(self, email: str = None, password: str = None, name: str = None, kindle_email: str = None) -> Dict[str, str]:
        return self.__makePostRequest('/eapi/user/update',
                                      {k: v for k, v in {"email": email, "password": password,
                                                         "name": name, "kindle_email": kindle_email}.items() if v is not None})

    def search(self, message: str = None, yearFrom: int = None, yearTo: int = None, languages: str = None, extensions: str = None, order: str = None, page: int = None, limit: int = None) -> Dict[str, str]:
        return self.__makePostRequest('/eapi/book/search',
                                      {k: v for k, v in {"message": message, "yearFrom": yearFrom,
                                                         "yearTo": yearTo, "languages": languages,
                                                         "extensions": extensions, "order": order,
                                                         "page": page, "limit": limit,
                                                         }.items() if v is not None})

    def __getImageData(self, url: str) -> requests.Response.content:
        path = url.split("books")[-1]
        for domain in self.__downloadDomains:
            url = "https://" + domain + "/covers/books" + path
            res = requests.get(url, headers=self.__headers,
                               cookies=self.__cookies)
            if res.status_code == 200:
                return res.content

    def getImage(self, book: Dict[str, str]) -> requests.Response.content:
        return self.__getImageData(book["cover"])

    def __getBookFile(self, bookid: Union[int, str], hashid: str):
        response = self.__makeGetRequest(f"/eapi/book/{bookid}/{hashid}/file")
        filename = response['file']['description']
        try:
            filename += " (" + response["file"]["author"] + ")"
        except:
            pass
        finally:
            filename += "." + response['file']['extension']
        token = response["file"]["downloadLink"].split("/dtoken/")[-1]

        for domain in self.__downloadDomains:
            dlink = "https://" + domain + "/dtoken/" + token
            res = requests.get(dlink, headers=self.__headers, cookies=self.__cookies)
            if res.status_code == 200:
                return filename, res.content

    def downloadBook(self, book: Dict[str, str]):
        return self.__getBookFile(book["id"], book["hash"])
