package com.thethreemusketeers.terminal.Activities;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
import android.util.Patterns;
import android.view.Gravity;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

import com.thethreemusketeers.terminal.JSONRequestObject.UserRegisterObject;
import com.thethreemusketeers.terminal.R;

public class CreateProfile3 extends AppCompatActivity {

    Button nextButton;
    LinearLayout studentRegisFields;
    EditText contactNumber;
    EditText emailAddr;
    EditText rollNo;
    EditText fatherName;
    EditText yearOfJoin;
    EditText yearOfPass;
    EditText programme;
    EditText branch;
    EditText section;
    EditText gender;
    EditText tempAddr;
    EditText permAddr;
    TextView attentionReqOnContactNumber;
    TextView attentionReqOnEmailAddr;
    TextView attentionReqOnRollNo;
    TextView attentionReqOnFatherName;
    TextView attentionReqOnYOJ;
    TextView attentionReqOnYOP;
    TextView attentionReqOnProgramme;
    TextView attentionReqOnBranch;
    TextView attentionReqOnSection;
    TextView attentionReqOnGender;
    TextView attentionReqOnTempAddress;
    TextView attentionReqOnPermAddress;
    boolean isEmailValidated = false, isContactNumberValidated = false;
    boolean isRollNoEmpty = true;
    boolean isFatherNameEmpty = true;
    boolean isYOJEmpty = true;
    boolean isYOPEmpty = true;
    boolean isProgrammeEmpty = true;
    boolean isBranchEmpty = true;
    boolean isSectionEmpty = true;
    boolean isGenderEmpty = true;
    boolean isTempAddrEmpty = true;
    boolean isPermAddrEmpty = true;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_create_profile3);

        // FETCHING COMPONENTS FROM XML FILE
        nextButton = findViewById(R.id.activity3_next_btn);
        studentRegisFields = findViewById(R.id.student_registration_fields);
        contactNumber = findViewById(R.id.contact_number);
        emailAddr = findViewById(R.id.email_address);
        yearOfJoin = findViewById(R.id.year_of_join);
        yearOfPass = findViewById(R.id.year_of_pass);
        programme = findViewById(R.id.programme);
        branch = findViewById(R.id.branch);
        section = findViewById(R.id.section);

        attentionReqOnContactNumber = findViewById(R.id.attention_required_on_contact_number_editText);
        attentionReqOnEmailAddr = findViewById(R.id.attention_required_on_email_address);
        attentionReqOnYOJ = findViewById(R.id.attention_required_on_year_of_join);
        attentionReqOnYOP = findViewById(R.id.attention_required_on_year_of_pass);
        attentionReqOnProgramme = findViewById(R.id.attention_required_on_programme);
        attentionReqOnBranch = findViewById(R.id.attention_required_on_branch);
        attentionReqOnSection = findViewById(R.id.attention_required_on_section);

        // PRESENTING USER INTERFACE BASED ON THE ACCOUNT-TYPE USER SELECTED
        if ( UserRegisterObject.account_type.equals(getString(R.string.account_type_faculty)) ){
            studentRegisFields.setVisibility(View.GONE);
        }
        else if ( UserRegisterObject.account_type.equals(getString(R.string.account_type_student)) ) {
            studentRegisFields.setVisibility((View.VISIBLE));
        }

        // CREATING EVENT LISTENERS

        // SETTING TEXT CHANGE LISTENER ON EMAIL ADDRESS FIELD
        emailAddr.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {

            }
            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {
                if ( s.equals("") ) {
                    attentionReqOnEmailAddr.setAlpha(0);
                    isEmailValidated = false;
                }
                else if ( Patterns.EMAIL_ADDRESS.matcher(s).matches() ) {
                    attentionReqOnEmailAddr.setAlpha(0);
                    isEmailValidated = true;
                }
                else {
                    attentionReqOnEmailAddr.setAlpha(1);
                    attentionReqOnEmailAddr.setText("(Invalid)");
                    isEmailValidated = false;
                }
            }
            @Override
            public void afterTextChanged(Editable s) {

            }
        });

        // SETTING EVENT LISTENER ON NEXT BUTTON
        nextButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // CHECKING WHETHER CONTACT NUMBER ISN'T EMPTY
                if( contactNumber.getText().toString().equals("") ) {
                    attentionReqOnContactNumber.setAlpha(1);
                    attentionReqOnContactNumber.setText("* Required");
                    isContactNumberValidated = false;
                }
                else {
                    attentionReqOnContactNumber.setAlpha(0);
                    attentionReqOnContactNumber.setText("* Required");
                    isContactNumberValidated = true;
                }
                // CHECKING WHETHER CONTACT NUMBER IS VALID OR NOT
                if( emailAddr.getText().toString().equals("") ) {
                    attentionReqOnEmailAddr.setAlpha(1);
                    attentionReqOnEmailAddr.setText("* Required");
                    isContactNumberValidated = false;
                }
                // EXECUTES WHEN USER ACCOUNT TYPE IS FACULTY
                if ( UserRegisterObject.account_type.equals(getString(R.string.account_type_faculty)) ) {
                    // EXECUTES WHEN EMAIL ADDRESS AND CONTACT NUMBER IS VALID/AREN'T EMPTY
                    if ( isEmailValidated && isContactNumberValidated ) {
                        UserRegisterObject.phone_number = contactNumber.getText().toString();
                        UserRegisterObject.email = emailAddr.getText().toString();
                        startActivity(new Intent(CreateProfile3.this,CreateProfile4.class));
                    }
                    else {
                        Toast toast = Toast.makeText(CreateProfile3.this,"Please fill all the required fields correctly",Toast.LENGTH_SHORT);
                        toast.setGravity(Gravity.CENTER_VERTICAL|Gravity.CENTER_HORIZONTAL,0,0);
                        toast.show();
                    }
                }

                // EXECUTES WHEN USER ACCOUNT TYPE IS STUDENT
                else if ( UserRegisterObject.account_type.equals(getString(R.string.account_type_student)) ) {
                    // CHECKING WHETHER YEAR OF JOIN ISN'T EMPTY
                    if( yearOfJoin.getText().toString().equals("") ) {
                        attentionReqOnYOJ.setAlpha(1);
                        attentionReqOnYOJ.setText("* Required");
                        isYOJEmpty = true;
                    }
                    else {
                        attentionReqOnYOJ.setAlpha(0);
                        attentionReqOnYOJ.setText("* Required");
                        isYOJEmpty = false;
                    }

                    // CHECKING WHETHER YEAR OF PASS ISN'T EMPTY
                    if( yearOfPass.getText().toString().equals("") ) {
                        attentionReqOnYOP.setAlpha(1);
                        attentionReqOnYOP.setText("* Required");
                        isYOPEmpty = true;
                    }
                    else {
                        attentionReqOnYOP.setAlpha(0);
                        attentionReqOnYOP.setText("* Required");
                        isYOPEmpty = false;
                    }

                    // CHECKING WHETHER PROGRAMME ISN'T EMPTY
                    if( programme.getText().toString().equals("") ) {
                        attentionReqOnProgramme.setAlpha(1);
                        attentionReqOnProgramme.setText("* Required");
                        isProgrammeEmpty = true;
                    }
                    else {
                        attentionReqOnProgramme.setAlpha(0);
                        attentionReqOnProgramme.setText("* Required");
                        isProgrammeEmpty = false;
                    }

                    // CHECKING WHETHER BRANCH ISN'T EMPTY
                    if( branch.getText().toString().equals("") ) {
                        attentionReqOnBranch.setAlpha(1);
                        attentionReqOnBranch.setText("* Required");
                        isBranchEmpty = true;
                    }
                    else {
                        attentionReqOnBranch.setAlpha(0);
                        attentionReqOnBranch.setText("* Required");
                        isBranchEmpty = false;
                    }

                    // CHECKING WHETHER SECTION ISN'T EMPTY
                    if( section.getText().toString().equals("") ) {
                        attentionReqOnSection.setAlpha(1);
                        attentionReqOnSection.setText("* Required");
                        isSectionEmpty = true;
                    }
                    else {
                        attentionReqOnSection.setAlpha(0);
                        attentionReqOnSection.setText("* Required");
                        isSectionEmpty = false;
                    }

                    // EXECUTES WHEN ALL FIELDS AREN'T EMPTY AND VALID
                    if ( isEmailValidated && isContactNumberValidated && !isYOJEmpty && !isYOPEmpty
                            && !isProgrammeEmpty && !isBranchEmpty && !isSectionEmpty ) {
                        UserRegisterObject.phone_number = contactNumber.getText().toString();
                        UserRegisterObject.email = emailAddr.getText().toString();
                        UserRegisterObject.year_of_join = yearOfJoin.getText().toString();
                        UserRegisterObject.year_of_pass = yearOfPass.getText().toString();
                        UserRegisterObject.programme = programme.getText().toString();
                        UserRegisterObject.branch = branch.getText().toString();
                        UserRegisterObject.section = section.getText().toString();
                        // SENDING BLANK STRING FOR NOT SO REQUIRED FIELDS
                        UserRegisterObject.rollno = "";
                        UserRegisterObject.father_name = "";
                        UserRegisterObject.gender = "";
                        UserRegisterObject.temp_addr = "";
                        UserRegisterObject.perm_addr = "";
                        // ROUTING TO IDENTITY PROOF IMAGE INPUT ACTIVITY
                        startActivity(new Intent(CreateProfile3.this,CreateProfile3A.class));
                    }
                    else {
                        Toast toast = Toast.makeText(CreateProfile3.this,"Please fill all the required fields correctly",Toast.LENGTH_SHORT);
                        toast.setGravity(Gravity.CENTER_VERTICAL|Gravity.CENTER_HORIZONTAL,0,0);
                        toast.show();
                    }
                }

            }
        });
    }
}
