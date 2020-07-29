# API Documentation

Request body and response body default format is JSON.
_____ 


`/api/token/`
 * `POST` Request Body : `email` and `password`
     * Response Body
     
         * On Success 
            * Access : Token String 
            * Refresh : Token String 
            
         * On Failure 
            * Status : 401
            * Detail : "No active account found with the given credentials"
        

`/api/courses/`
 * `GET` Request Body : `email` and `password`
 * Response Body
 
     * On Success 
        * An array of "Course" objects (id: string, name: string)
        
     * On Failure 
        * Status : 401
        * Detail : "Given token not valid for any token type"
"
    