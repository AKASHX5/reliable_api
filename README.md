##ASUMPTIONS:
    The server has endpoint like below which handles both POST and DELETE request
```python
@routes.route('/v1/group/two', methods=['POST',"DELETE"])
def group_two():

    if request.method == 'POST':
        # Handle creation
        data = request.json
        # Process the data and create the resource
        # For example, save the data to a database
        response = {"message": "Resource created", "data": data}
        return jsonify(response), 201

    elif request.method == 'DELETE':
        # Handle deletion
        # Get the parameters from the request
        resource_id = request.args.get('groupId')
        # Process the resource_id to delete the resource
        # For example, remove the resource from the database
        if resource_id:
            response = {
                "message": f"Resource with id {resource_id} deleted"}
            return jsonify(response), 200
        else:
            return jsonify({"error": "Resource ID is required"}), 400
```
    A post API is called from the client which hits the server the body of the api
    the DELETE API also contains body which is used to construct a url with params 
    httpx does not support adding body to the request so the request is parsed 
    and a url like http://localhost:5001/v1/group/one?groupId=123 is constructed to perform the delete operation

#SOLUTION
    Based on the assumptions the solutions in designed like mentioned below
    - A create_group or delete api is called with the json data
    - it iterated through the list of nodes and performs action
    - upon failure it roll backs( deletes or creates) the data that are being created
    - if it fails to perform rollback there is a retry mechanism which the user can design on how many times the system should try to perform the action
    - and the retry is backed with exponential backoff algorithm to ensure network congestion taken care of

##TESTING STRATIGIES

#### Test Cases for create_group_api
- Test Case: Successful Creation of Group in All Nodes
- Test Case: Failure to Create Group in Any Node
- Test Case: Partial Success Leading to Rollback
- Test Case: Invalid groupId in Request
- Test Case: Endpoint Not Found During Creation

#### Test Cases for delete_group_api
- Test Case: Successful Deletion of Group in All Nodes
- Test Case: Failure to Delete Group in Any Node
- Test Case: Partial Success Leading to Rollback
- Test Case: Invalid groupId in Request
- Test Case: Endpoint Not Found During Deletion

### HOW TO RUN THE CODE
 - `chmod +x k8.sh`
 - `minikube service realiable-api-service`
 - `http://127.0.0.1:64891/v1/delete_groups`
 - `http://127.0.0.1:64891/v1/create_groups`

### IMPROVEMENTS
- iterating the list of nodes asynchornusly 
- using dataclass to add typing
- sending alert to slack when the pod goes down.