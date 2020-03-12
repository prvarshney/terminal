package com.thethreemusketeers.terminal;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.graphics.Color;
import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Spinner;
import android.widget.TextView;

public class CreateProfile1 extends AppCompatActivity {

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
        adapter.setDropDownViewResource(R.layout.spinner_text);
        accountTypeDropDown.setAdapter(adapter);

        // SETTING EVENT LISTENERS
        // THIS EVENT LISTENER OFF THE REQUIRED WARNING OVER COMPLETE USERNAME EDIT TEXT BOX
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

        // THIS EVENT LISTENER ROUTES TO OTHER ACTIVITIES BASED ON THE ACCOUNT TYPE USER SELECTED
        nextBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // CHECKING WHETHER ALL FIELDS ARE FILED WITH USERDATA OR NOT
                String usernameValue = username.getText().toString();
                String accountType = accountTypeDropDown.getSelectedItem().toString();
                Boolean proceedingNextFlag = true;
                if(usernameValue.equals("")) {
                    attentionRequiredTowardsUsernameField.setAlpha(1);
                    proceedingNextFlag = false;
                }
                else
                    attentionRequiredTowardsUsernameField.setAlpha(0);

                if(accountType.equals("Select Account-Type")) {
                    attentionRequiredTowardsAccountTypeField.setAlpha(1);
                    proceedingNextFlag = false;
                }
                else
                    attentionRequiredTowardsAccountTypeField.setAlpha(0);

                if( proceedingNextFlag ){
                    // PROCEEDING FURTHER TO ACTIVITY_CREATE_PROFILE2 ONLY WHEN USER IS A FACULTY
                    if ( accountType.equals("Faculty (BPIT)") )
                        startActivity(new Intent(CreateProfile1.this,CreateProfile2.class));
                    // PROCEEDING FURTHER TO ACTIVITY_CREATE_PROFILE3 WHEN USER IS NOT A FACULTY
                    else
                        startActivity(new Intent(CreateProfile1.this,MainActivity.class));
                }
            }
        });
    }
}
