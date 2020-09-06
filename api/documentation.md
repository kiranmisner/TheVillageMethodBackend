# API Documentation
### Details the various endpoints supported by this backend framework.
### Request body and response body default format is JSON.
_____ 

## `/api/createuser/`
### `POST`
* Request Body
   * `email`: string (valid email address)
   * `password`: string
   * `name`: string
   * `school`: string (Salesforce ID)
* Response Body
   * On Success 
      * The successfully created "User" object 
         * `id`: string (UUID)
         * `name`: string
         * `email`: string (valid email address)
         * `school`: string (Salesforce ID)
      * *Note: The School property refers to the Salesforce ID for a particular school*
   * On Failure
      * `Status`: 400
      * `Detail`: "user with this email address already exists."
_____

## `/api/token/`
### `POST`
* Request Body
   * `email`: string (valid email address)
   * `password`: string
* Response Body
   * On Success 
      * `Access`: string (access token)
      * `Refresh`: string (refresh token)
   * On Failure 
      * `Status`: 401
      * `Detail`: "No active account found with the given credentials"
_____  

## `/api/schools/`
### `GET`
* Request Headers
   * Authorization: Bearer `<Access Token>`
* Request Body
   * None
* Response Body
   * On Success 
      * An array of all existing "School" objects
         * `id`: string (Salesforce ID)
         * `name`: string
         * `institution_type`: string
         * `school_id`: string (A-G School ID)
         * `city`: string
         * `state`: string
         * `website_id`: int (A-G Website ID)
   * On Failure 
      * `Status`: 401
      * `Detail`: "Given token not valid for any token type"
_____

## `/api/schools/<pk>`
### `GET`
* Request Headers
   * Authorization: Bearer `<Access Token>`
* Request Body
   * None
* Response Body
   * On Success 
      * The "School" object with a matching primary key specified in the URL
         * `id`: string (Salesforce ID)
         * `name`: string
         * `institution_type`: string
         * `school_id`: string (A-G School ID)
         * `city`: string
         * `state`: string
         * `website_id`: int (A-G Website ID)
      * *Note: The primary key for a "School" object is its Salesforce ID*
   * On Failure 
      * `Status`: 401
      * `Detail`: "Given token not valid for any token type"
_____

## `/api/courses/`
### `GET`
* Request Headers
   * Authorization: Bearer `<Access Token>`
* Request Body
   * None
* Response Body
   * On Success 
      * An array of all existing "Course" objects
         * `id`: string (Salesforce ID)
         * `name`: string
         * `school`: string (Salesforce ID)
         * `is_honors`: bool
         * `provider`: string
         * `academic_years`: string (semicolon separated list of strings)
         * `grade_levels`: string (semicolon separated list of strings)
         * `course_length`: string
         * `transcript_abbs`: string (semicolon separated list of strings)
         * `subject`: string
         * `ag_designation`: string (letter from A to G)
   * On Failure 
      * `Status`: 401
      * `Detail`: "Given token not valid for any token type"
_____ 

## `/api/courses/<pk>`
### `GET`
* Request Headers
   * Authorization: Bearer `<Access Token>`
* Request Body
   * None
* Response Body
   * On Success 
      * The "Course" object with a matching primary key specified in the URL
         * `id`: string (Salesforce ID)
         * `name`: string
         * `school`: string (Salesforce ID)
         * `is_honors`: bool
         * `provider`: string
         * `academic_years`: string (semicolon separated list of strings)
         * `grade_levels`: string (semicolon separated list of strings)
         * `course_length`: string
         * `transcript_abbs`: string (semicolon separated list of strings)
         * `subject`: string
         * `ag_designation`: string (letter from A to G)
      * *Note: The primary key for a "Course" object is its Salesforce ID*
   * On Failure 
      * `Status`: 401
      * `Detail`: "Given token not valid for any token type"
_____ 

## `/api/schoolcourses/`
### `GET`
* Request Headers
   * Authorization: Bearer `<Access Token>`
* Request Body
   * None
* Response Body
   * On Success 
      * An array of objects containing arrays of "Course" objects associated with each "School" object
         * `course_set`: array of "Course" objects
   * On Failure 
      * `Status`: 401
      * `Detail`: "Given token not valid for any token type"
_____ 

## `/api/schoolcourses/<pk>`
### `GET`
* Request Headers
   * Authorization: Bearer `<Access Token>`
* Request Body
   * None
* Response Body
   * On Success 
      * An object containing an array of "Course" objects associated with the "School" object with a matching primary  
        key specified in the URL
         * `course_set`: array of "Course" objects
   * On Failure 
      * `Status`: 401
      * `Detail`: "Given token not valid for any token type"