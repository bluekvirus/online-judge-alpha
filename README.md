<<<<<<< HEAD
# online-judge-backend
## Docker-Compose.yml
Please use the provided docker-compose.yml file.
## RESTFUL API METHODS
1) To submit to Hackerrank, send a POST request to http://localhost:8000/api/v1/postSubmission with json payload body in the form of:

EXAMPLE: 
  ```
  { 
    "code":"#!/bin/python3\n\nimport os\nimport sys\n\n#\n# 
    Complete the simpleArraySum function below.\n#\ndef simpleArraySum(ar):\n    #\n   
    # Write your code here.\n    #\n    return sum(ar)\n\nif __name__ == '__main__':\n    
    fptr = open(os.environ['OUTPUT_PATH'], 'w')\n\n    ar_count = int(input())\n\n    
    ar = list(map(int, input().rstrip().split()))\n\n  
    result = simpleArraySum(ar)\n\n    fptr.write(str(result) + '\\n')\n\n    fptr.close()\n",
    "language":"python3", "problem-name" : "simple-array-sum", "user_id": 2
  }
  ```
*Required Keys*: "code", "language", "problem-name", "user_id"

2) To get all submission results for a specific user id, send a GET request to 
http://localhost:8000/api/v1/getResults?uid=_________

3) To get all submission results for a specific user id with a specific problem name, send a GET request to http://localhost:8000/api/v1/getResults?uid=__________&problem=___________
=======
# CodingJudgePlatform

>>>>>>> 5f7917d4ef90fe274c8268dec54e7a8c5eb08916
