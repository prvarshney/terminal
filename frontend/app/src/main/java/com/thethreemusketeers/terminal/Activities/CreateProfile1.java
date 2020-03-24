package com.thethreemusketeers.terminal.Activities;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
import android.view.Gravity;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import com.thethreemusketeers.terminal.JSONRequestObject.UserRegisterObject;
import com.thethreemusketeers.terminal.R;

public class CreateProfile1 extends AppCompatActivity {

    // DECLARING VARIABLES
    Spinner accountTypeDropDown;
    Button nextBtn;
    EditText username;
    TextView attentionRequiredTowardsUsernameField, attentionRequiredTowardsAccountTypeField;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_create_profile1);

        // FETCHING XML ELEMENTS
        accountTypeDropDown = findViewById(R.id.account_type_dropdown);
        nextBtn = findViewById(R.id.activity1_next_btn);
        username = findViewById(R.id.username);
        attentionRequiredTowardsUsernameField = findViewById(R.id.attention_required_on_username_editText);
        attentionRequiredTowardsAccountTypeField = findViewById(R.id.attention_required_on_accountType_spinner);

        // INITIALIZATION OF UserRegisterObject WITH EMPTY STRING SO THAT LAST SESSION VALUES AREN'T
        // USE IN THIS SESSION
        UserRegisterObject.account_type = "";
        UserRegisterObject.name = "";
        UserRegisterObject.enrollment = "";
        UserRegisterObject.rollno = "";
        UserRegisterObject.year_of_pass = "";
        UserRegisterObject.year_of_join = "";
        UserRegisterObject.programme = "";
        UserRegisterObject.section = "";
        UserRegisterObject.branch = "";
        UserRegisterObject.temp_addr = "";
        UserRegisterObject.perm_addr = "";
        UserRegisterObject.father_name = "";
        UserRegisterObject.gender = "";
        UserRegisterObject.faculty_id = "";
        UserRegisterObject.phone_number = "";
        UserRegisterObject.email = "";
        UserRegisterObject.password = "";
        UserRegisterObject.dob = "";

        // SETTING DROPDOWN ELEMENTS
        String[] accountTypeDropDownElements = new String[]{"Select Account-Type","Student (BPIT)","Faculty (BPIT)"};
        ArrayAdapter<String> adapter = new ArrayAdapter<String>(this,R.layout.spinner_dropdown ,accountTypeDropDownElements){
            @Override
            public boolean isEnabled(int position) {
                if (position == 0)
                    return false;
                else {
                    attentionRequiredTowardsAccountTypeField.setAlpha(0);
                    return true;
                }
            }
        };
        adapter.setDropDownViewResource(R.layout.spinner_text_layout_for_create_profile1);
        accountTypeDropDown.setAdapter(adapter);

        // SETTING EVENT LISTENERS
        // THIS EVENT LISTENER OFF THE REQUIRED WARNING OVER FULL NAME EDIT TEXT BOX
        // WHEN THEIR IS SOME TEXT INSIDE EDIT TEXT BOX
        username.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {

            }
            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {
                if( !s.equals("") )
                    attentionRequiredTowardsUsernameField.setAlpha(0);
            }
            @Override
            public void afterTextChanged(Editable s) {

            }
        });

        // THIS EVENT LISTENER RECORDS USER INPUT AND ROUTES TO OTHER ACTIVITIY
        nextBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // CHECKING WHETHER ALL FIELDS ARE FILED WITH USERDATA OR NOT
                String usernameValue = username.getText().toString();
                String accountType = accountTypeDropDown.getSelectedItem().toString();
                Boolean isUsernameValid, isAccountTypeValid;
                // VALIDATING USERNAME FIELD
                if(usernameValue.equals("")) {
                    attentionRequiredTowardsUsernameField.setAlpha(1);
                    isUsernameValid = false;
                }
                else {
                    attentionRequiredTowardsUsernameField.setAlpha(0);
                    isUsernameValid = true;
                }
                // CHECKING WHETHER ACCOUNT-TYPE FIELD IS SELECTED OR NOT
                if(accountType.equals("Select Account-Type")) {
                    attentionRequiredTowardsAccountTypeField.setAlpha(1);
                    isAccountTypeValid = false;
                }
                else {
                    attentionRequiredTowardsAccountTypeField.setAlpha(0);
                    isAccountTypeValid = true;
                }
                // EXECUTES WHEN BOTH FIELDS ARE VALIDATED
                if( isUsernameValid && isAccountTypeValid ){
                    // STORING USER INPUT VALUES IN USER_REGISTER_OBJECT (STATIC)
                    if ( accountType.equals("Faculty (BPIT)") )
                        UserRegisterObject.account_type = getString(R.string.account_type_faculty);
                    else if ( accountType.equals("Student (BPIT)") )
                        UserRegisterObject.account_type = getString(R.string.account_type_student);
                    UserRegisterObject.name = usernameValue;
                    startActivity(new Intent(CreateProfile1.this,CreateProfile2.class));
                }
                else {
                    // EXECUTES WHEN EITHER FIELD OR BOTH FIELDS ARE INVALID
                    Toast toast = Toast.makeText(CreateProfile1.this,"Please fill all the required fields",Toast.LENGTH_SHORT);
                    toast.setGravity(Gravity.CENTER_VERTICAL|Gravity.CENTER_HORIZONTAL,0,0);
                    toast.show();
                }
            }
        });
    }
}
