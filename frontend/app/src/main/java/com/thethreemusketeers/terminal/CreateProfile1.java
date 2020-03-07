package com.thethreemusketeers.terminal;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.graphics.Color;
import android.os.Bundle;
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

        // fetching xml elements
        accountTypeDropDown = findViewById(R.id.account_type_dropdown);
        nextBtn = findViewById(R.id.next_btn);
        username = findViewById(R.id.username);
        attentionRequiredTowardsUsernameField = findViewById(R.id.attention_required_on_username_editText);
        attentionRequiredTowardsAccountTypeField = findViewById(R.id.attention_required_on_accountType_spinner);

        // setting dropdown elements
        String[] accountTypeDropDownElements = new String[]{"Select Account-Type","Student (BPIT)","Faculty (BPIT)"};
        ArrayAdapter<String> adapter = new ArrayAdapter<String>(this,R.layout.spinner_dropdown ,accountTypeDropDownElements){
            @Override
            public boolean isEnabled(int position) {
                if (position == 0)
                    return false;
                else
                    return true;
            }

        };
        adapter.setDropDownViewResource(R.layout.spinner_text);
        accountTypeDropDown.setAdapter(adapter);

        // setting event listeners
        nextBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // checking whether all fields are filled by userdata or not
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
                    //proceeding to further
                    startActivity(new Intent(CreateProfile1.this,MainActivity.class));
                }
            }
        });
    }
}
