package com.thethreemusketeers.terminal.Activities;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

import com.thethreemusketeers.terminal.R;

public class CreateProfile4 extends AppCompatActivity {

    Button nextBtn;
    EditText password, confirmPassword;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_create_profile4);

        // FETCHING ELEMENTS FROM LAYOUT DESIGN
        nextBtn = findViewById(R.id.activity4_next_btn);
        password = findViewById(R.id.registration_password_editText);
        confirmPassword = findViewById(R.id.registration_confirm_password_editText);

        // CREATING EVENT LISTENERS
        nextBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if( password.getText().toString().equals(confirmPassword.getText().toString()) && isValidPassword(password.getText().toString())) {
                    
                }
            }
        });
    }

    public static boolean isValidPassword(String password){
        return true;
    }

}
