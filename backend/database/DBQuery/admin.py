from pymongo import MongoClient
import config
import sys
from logger import log

## START OF ADMIN COLLECTION API
## -------------------------------------------------------------------------------------------------
## THIS ADMIN CLASS IS USED FOR THE FOLLOWING FUNCTIONS:-
## 1. QUERYING ADMIN PROFILE PASSWORD WITH METHOD NAME - QUERY
## 2. UPDATING ADMIN PROFILE PASSWORD WITH METHOD NAME - UPDATE
##
class Admin:
    def __init__(self):
        try:
            self.client = MongoClient(config.MongoDB_URI)
            db = self.client[config.Admin_DB]
            log(f'[  INFO  ] {config.Admin_DB} Connected Successfully')
        except:
            log(f'[  ERROR ] Unable To Create Connection With {config.Admin_DB}')
        self.collection = db[config.Admin_Profile_Collection]
        # document = {
        #    'adminid': 'ADM0123456AXY',
        #    'password': 'ADMqwertyuiop12'
        # }

    def query(self,query_parameter,query_value):
        # THIS QUERY FUNCTION INPUTS QUERY PARAMETER LIKE USERID AND QUERY VALUE TO SEARCH THE PASSWORD
        # IN COLLECTION.  AFTER SUCCESSFUL SEARCH, IT RETURNS
        # -----------------------------------------------------
        # DATA STRUCTURE OF INPUT PARAMETER :-
        # QUERY_PARAMETER --> STRING
        # QUERY_VALUE --> STRING
        #
        res = self.collection.find({ query_parameter: query_value})
        if res.count() > 0:     ## RUNS WHEN ANY RESULT COMES
            response = {
                'status': 212,
                'res': res
            }
        else: 
            response = {
                'status':206,
                'res': None
            }
        log(f'[  INFO  ] The Search Query Completed Successfully in {config.Admin_DB}')
        return response

    def update_password(self,admin_id,password):
        # THIS UPDATE FUNCTION UPDATES THE UPDATION_PARAM WITH THE UPDATION_VALUE
        # ------------------------------------------------------------------------
        # DATA STRUCTURES FOR INPUT PARAMETERS:-
        # UPDATION_PARAM --> STRING
        # PASSWORD --> STRING
        #
        searching_values = { 'admin_id':admin_id }
        updating_values = { 'password':password }
        try:
            status = self.collection.update_one(searching_values, {'$set':updating_values})
            log(f'[  INFO  ] {status}')
            log(f'[  INFO  ] Password Updation Completed Successfully in {config.Admin_DB}')
            return 301
        except:
            log(f'[  ERROR ] Password Updation Failed in {config.Admin_DB}')
            return 204

    def __del__(self):
        self.client.close()


if __name__ == "__main__":
    # TEST CODE COMES HERE
    pass
