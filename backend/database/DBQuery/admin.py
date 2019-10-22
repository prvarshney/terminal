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
            log('[  INFO  ] Admin_DB connected successfully.')
        except:
            log('[  ERROR  ] Unable to create connection with Admin_DB.')
            sys.exit(0)
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
        try:
            res = list(self.collection.find({ query_parameter: query_value}))
            response = {
                'status': '212',
                'res': res
            } 
        except:
            response = {
                'status':'206',
                'res':res
            }
        log('[ INFO  ] The search query is successfully completed.')
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
            log(f'[ INFO  ] {status}')
            log('[ INFO  ] Admin_DB has been updated.')
            return 301
        except:
            log('[ ERROR  ] Updation failed.')
            return 204

    def __del__(self):
        self.client.close()


if __name__ == "__main__":
    # TEST CODE COMES HERE
    admin = Admin()
    admin.update_password('adm-123','efkwfwlwf')
    admin.query('admin_id','adm-123')
    pass
