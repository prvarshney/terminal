package com.thethreemusketeers.terminal.Activities;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
import android.util.Patterns;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import com.thethreemusketeers.terminal.JSONRequestObject.FacultyRegisterObject;
import com.thethreemusketeers.terminal.R;

public class CreateProfile3 extends AppCompatActivity {

    Button nextButton;
    EditText contactNumber;
    EditText emailAddr;
    TextView attentionReqOnContactNumber;
    TextView attentionReqOnEmailAddr;
    boolean isEmailValidated, isContactNumberValidated;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_create_profile3);

        // FETCHING COMPONENTS FROM XML FILE
        nextButton = findViewById(R.id.activity3_next_btn);
        contactNumber = findViewById(R.id.contact_number);
        emailAddr = findViewById(R.id.email_address);
        attentionReqOnContactNumber = findViewById(R.id.attention_required_on_contact_number_editText);
        attentionReqOnEmailAddr = findViewById(R.id.attention_required_on_email_address);

        // CREATING EVENT LISTENERS
        // SETTING TEXT CHANGE LISTENER ON CONTACT NUMBER FIELD
        contactNumber.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {

            }
            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {
                if( s.toString().length() != 10 ) {
                    attentionReqOnContactNumber.setAlpha(1);
                    attentionReqOnContactNumber.setText("(Invalid)");
                    isContactNumberValidated = false;
                }
                else {
                    attentionReqOnContactNumber.setAlpha(0);
                    isContactNumberValidated = true;
                }
            }
            @Override
            public void afterTextChanged(Editable s) {

            }
        });
        // SETTING TEXT CHANGE LISTENER ON EMAIL ADDRESS FIELD
        emailAddr.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {

            }
            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {
                if ( Patterns.EMAIL_ADDRESS.matcher(s).matches() ) {
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
                // CHECKING WHETHER CONTACT NUMBER IS VALID OR NOT
                if( contactNumber.getText().toString().equals("") ) {
                    attentionReqOnContactNumber.setAlpha(1);
                    attentionReqOnContactNumber.setText("* Required");
                    isContactNumberValidated = false;
                }
                if( emailAddr.getText().toString().equals("") ) {
                    attentionReqOnEmailAddr.setAlpha(1);
                    attentionReqOnEmailAddr.setText("* Required");
                    isContactNumberValidated = false;
                }
                if ( isEmailValidated && isContactNumberValidated ) {
                    FacultyRegisterObject.phone_number = contactNumber.getText().toString();
                    FacultyRegisterObject.email = emailAddr.getText().toString();
                    startActivity(new Intent(CreateProfile3.this,CreateProfile4.class));
                }
            }
        });
    }
}
