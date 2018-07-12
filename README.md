# Online Coding Judge Container
## What is Online Coding Judge Container
Our online coding judge docker container, encapsulates a fully functioning backend which delegates the online judging of coding challenges to three judges we have chosen. This allows any front-end design to be used with our simple API.

## Quick Start 
By utilizing Docker containers, the startup procedure is greatly simplified. 
Please follow these steps to begin using the container for your frontend coding platform needs. 

 1. Download or clone this repo
  `git clone https://cmhuang2704@bitbucket.org/cmhuang2704/codingjudgeplatform.git .`
  2. Start up docker services </br>
    `docker-compose build` </br>
    `docker-compose up`
 3. Test
    Once the services are up, go to `localhost:8000/interview/hello`  to make sure it is up and running.
    
## Usage

### Admin Site
**1. Access Admin Site**
To easily create interviews and candidates in the online judge database, visit the admin site at `localhost:8000/admin`.  The default username is `admin` and the default password is `hackerrank`. In order to change the default username and password, please `cd myhackerrank` and follow Django 2.0 directions in creating a superuser using `manage.py`. 

**2. Add Candidates**
Once you have logged in successfully into the admin site, select **Add** next to Candidates under the MyServices tab.  Enter in the candidates email into the user name text box and click save. A timestamp will be automatically created, marking the time the candidate was added. 

**3. Create Interviews**
From the home page of the admin site, select  **Add** next to Interview under the MyServices tab. Select a status in the dropdown, typically this will be draft when the Interview is first created. Then select an existing candidate or add a new candidate. Then choose as many problems as you would like for this interview. *Note:* Problems are easily added using the add_problems.py script. Details below in the next section. The hash string used to uniquely identify the interview, as well as the created-at and started-at timestamps will be automatically generated once the interview is saved.

**4. Add Problems**
There is no need to use the admin site to add problems. Instead, place all of your html problem descriptions inside of the problems folder. An example would be `/myhackerrank/problems/**difficulty**/problem-name.html`. In order to populate the database with new problems, go into `/myhackerrank` and run `python add_problems.py`. This script will automatically add the problem name, the path to the problem html file, and the difficulty. By following this folder structure for the problems folder, the backend will automatically create tabs holding the problem descriptions you have chosen for a particular interview. 

### How To Access The Interview 
There are two ways in which a candidate can access the interview. If there is anything wrong with the request, a 404 page will be displayed.
1) To **GET** the interview, if the candidate knows their unique interview hash string, directly access `http://localhost:8000/interview/**hashstr**`.

2) If the candidate email is known instead, **GET** at `http://localhost:8000/`. This will present the candidate with a simple form that takes in their email. If the candidate has multiple interviews assigned to them, any "Completed" interviews are filtered out, and the interview with the oldest created_at timestamp is rendered and displayed to the candidate. 

### RESTFUL API METHODS
1) To **submit** to Hackerrank, send a POST request to `http://localhost:8000/interview/**hashstr**/submit` with json payload body.  It must have the required keys: "code", "language", "pid". "pid" is the problem id for a specific interview problem, as stored in the database. When the html page for a problem is rendered server side  the `.text-pane`, `.result-pane`, and `.submit-btn` will be embedded with a `data-problem-id` attribute. This is to allow  any front end to be able to easily identify which problem id the current tab is associated with. 

Example: 
  ```
  { 
    "code":"#!/bin/python3\n\nimport os\nimport sys\n\n#\n# 
    Complete the simpleArraySum function below.\n#\ndef simpleArraySum(ar):\n    #\n   
    # Write your code here.\n    #\n    return sum(ar)\n\nif __name__ == '__main__':\n    
    fptr = open(os.environ['OUTPUT_PATH'], 'w')\n\n    ar_count = int(input())\n\n    
    ar = list(map(int, input().rstrip().split()))\n\n  
    result = simpleArraySum(ar)\n\n    fptr.write(str(result) + '\\n')\n\n    fptr.close()\n",
    "language":"python3", "pid" : 1
  }
  ```

2) To retrieve all submission **results** for a specific interview, send a GET request to :
`http://localhost:8000/interview/**hashstr**/results`

3) To retrieve all submission **results** for a specific interview **and** specific problem, send a GET request to :
`http://localhost:8000/interview/**hashstr**/results?pid=___`
The `pid` query parameter is the problem id.

4) To **start an interview session**  (e.g when the candidate clicks the start button), send a GET request to :
`http://localhost:8000/interview/**hashstr**/start`
This will automatically set the started_at timestamp for the interview, which will be used to validate that an interview has not exceeded the allotted time period. It will also change the state of the interview to `Started`.

5) To **retrieve the start time** timestamp of the interview, send a GET request to :
`http://localhost:8000/interview/**hashstr**/time`
This can be used to calculate and create a cosmetic front-end timer, thus allowing candidates to see how much time they have left.

6) To **poll for results** in the case that the returned result is "Queued" or "Processing", you can use this api within your polling logic. Send a GET request to :
`http://localhost:8000/interview/**hashstr**/poll?pid=___&sid=___`
`pid` is the  problem id and `sid` is the submission id which was generated and returned when a submission was made to the submit api.

7) **To get problems and html pages**: The main benefit of this online judge backend container, is the server-side rendered html pages. They will automatically create tabs, code editors, result panes,  etc which can be used directly in your front-end. All you need is an empty `<div></div>` container to display. The main api which will display either a 404 not found page for invalid interviews, a welcome page for un-started valid interviews, or the problems and coding page for started valid interviews. All your front-end has to do is send a GET request to the problems api:
`http://localhost:8000/interview/**hashstr**/problems`

8) To **test** that the server is up and running, send a GET request to
`http://localhost:8000/interview/hello`

## MODELS
 **Models: Interview, Candidate, Problem, Submission**
 
*Note:* A candidate can have many interviews, but an interview can only have one candidate. An interview can have as many problems as desired, and a problem can belong to as many interviews as necessary. An interview can also have many submission instances but submissions will belong to the respective interview and thus candidate.

