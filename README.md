# pwap-api

Example requests can be found in `requests.http`

**API Endpoints**

* **URL**

  /task

* **Method:**
  
  `GET`

-----------------------------------------------------

* **URL**

  /task

* **Method:**
  
  `POST`
  
*  **DATA(body) Params**  
    `name=[string]`  
    `description=[string]`
    `password=[string]`

-----------------------------------------------------

* **URL**

  /task/<id>

* **Method:**
  
  `GET`
  
*  **URL Params**
    
    `Id=[integer]`  
  
-----------------------------------------------------

* **URL**

  /task/<id>

* **Method:**
  
  `DELETE`
  
*  **URL Params**
    
    `Id=[integer]`  
  
  *  **DATA Params**
  
    `password=[string]`
  
  -----------------------------------------------------

* **URL**

  /task/<id>

* **Method:**
  
  `PUT`
  
*  **URL Params**
    
    `Id=[integer]`  
  
  *  **DATA Params**
  
    `password=[string]`
    `name=[string]`
    `description=[string]`
  
