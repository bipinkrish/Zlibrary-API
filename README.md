# Zlibrary-API

Unofficial Zlibarary API for Python. No need for Libraries, just copy ```Zlibrary.py``` file to your project directory, one File can handle all your requests.

Only dependency is ```requests``` you can install it using 

```
pip install requests
```

---

# Documentation

## Importing
```
from Zlibrary import Zlibrary
```

## Logging in

* ### while creating object
```
Z = Zlibrary(email="xxx@mail.com", password="password") # using mail and password

# OR

Z = Zlibrary(remix_userid="12345", remix_userkey="abcdef") # using remix id and keys
```
* ### after object creation
```
Z = Zlibrary()

Z.login(email="xxx@mail.com", password="password") # using mail and password

# OR

Z.loginWithToken(remix_userid="12345", remix_userkey="abcdef") # using remix id and keys
```

## Availabale Methods

```
getProfile() -> Dict[str, str]
```

```
getMostPopular(switch_language: str = None) -> Dict[str, str]
```

```
getRecently() -> Dict[str, str]
```

```
getUserRecommended() -> Dict[str, str]
```

```
deleteUserBook(bookid: Union[int, str]) -> Dict[str, str]
```

```
unsaveUserBook(bookid: Union[int, str]) -> Dict[str, str]
```

```
getBookForamt(bookid: Union[int, str], hashid: str) -> Dict[str, str]
```

```
getDonations() -> Dict[str, str]
```

```
getUserDownloaded(order: str = None, page: int = None, limit: int = None) -> Dict[str, str]
```

```
getExtensions() -> Dict[str, str]
```

```
getDomains() -> Dict[str, str]
```

```
getLanguages() -> Dict[str, str]
```

```
getPlans(switch_language: str = None) -> Dict[str, str]
```

```
getUserSaved(order: str = None, page: int = None, limit: int = None) -> Dict[str, str]
```

```
getInfo(switch_language: str = None) -> Dict[str, str]
```

```
hideBanner() -> Dict[str, str]
```

```
recoverPassword(email: str) -> Dict[str, str]
```

```
makeRegistration(email: str, password: str, name: str) -> Dict[str, str]
```

```
resendConfirmation() -> Dict[str, str]
```

```
saveBook(bookid: Union[int, str]) -> Dict[str, str]
```

```
sendTo(bookid: Union[int, str], hashid: str, totype: str) -> Dict[str, str]
```

```
getBookInfo(bookid: Union[int, str], hashid: str, switch_language: str = None) -> Dict[str, str]
```

```
getSimilar(bookid: Union[int, str], hashid: str) -> Dict[str, str]
```

```
makeTokenSigin(name: str, id_token: str) -> Dict[str, str]
```

```
updateInfo(email: str = None, password: str = None, name: str = None, kindle_email: str = None) -> Dict[str, str]
```

```
search(message: str = None, yearFrom: int = None, yearTo: int = None, languages: str = None, extensions: str = None, order: str = None, page: int = None, limit: int = None) -> Dict[str, str]
```

```
getImage(book: Dict[str, str]) -> requests.Response.content
```

```
downloadBook(book: Dict[str, str]) -> List[str, requests.Response.content]
```

---

# Examples

* ### Getting image
```
from Zlibrary import Zlibrary

# Create Zlibrary object and login
Z = Zlibrary(email="xxx@mail.com", password="password")

# Search for books
results = Z.search(message='The Great Gatsby')

# Getting image content
imgcont = Z.getImage(results["books"][0])

# Writting image content to a file
with open("img.jpg", "wb") as imgfile:
    imgfile.write(imgcont)
```

* ### Downloading a book
```
from Zlibrary import Zlibrary

# Create Zlibrary object and login
Z = Zlibrary(email="xxx@mail.com", password="password")

# Get most popular books
most_popular = Z.getMostPopular()

# Downloading a book
filename, filecont = Z.downloadBook(most_popular["boooks][0])

# Writting file content to a file
with open(filename, "wb") as bookfile:
    bookfile.write(filecont)
```

---

# Credits for Endpoints

* [zlibrary-eapi-documentation](https://github.com/baroxyton/zlibrary-eapi-documentation)
