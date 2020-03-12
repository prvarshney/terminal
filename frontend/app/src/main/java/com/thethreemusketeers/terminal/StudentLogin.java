package com.thethreemusketeers.terminal;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.text.method.PasswordTransformationMethod;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.TextView;

public class StudentLogin extends AppCompatActivity {

    EditText passwordEditText, userId ;
    TextView attentionRequiredTowardsUsernameField, attentionRequiredTowardsPasswordTypeField;
    ImageView passwordEye;
    Boolean eyeTogglerFlag = true;
    Button loginBtn;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_student_login);

        passwordEditText = findViewById(R.id.password_edit_text);
        passwordEye = findViewById(R.id.password_eye);
        userId = findViewById(R.id.userid);
        loginBtn = findViewById(R.id.login_btn);
        attentionRequiredTowardsUsernameField = findViewById(R.id.attention_required_on_username_editText);
        attentionRequiredTowardsPasswordTypeField = findViewById(R.id.attention_required_on_password_editText);

        //setting event listeners
        passwordEye.setOnClickListener((new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                if(eyeTogglerFlag){
                    passwordEditText.setTransformationMethod(null);
                    eyeTogglerFlag = false;
                    passwordEye.setImageResource(R.drawable.password_eye_crossed);
                } else{
                    passwordEditText.setTransformationMethod(new PasswordTransformationMethod());
                    eyeTogglerFlag = true;
                    passwordEye.setImageResource(R.drawable.password_eye);
                }
            }
        })
        );

        //setting event listeners
        loginBtn.setOnClickListener((new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String usernameValue = userId.getText().toString();
                String passwordValue = passwordEditText.getText().toString();
                Boolean proceedingNextFlag = true;
                if (usernameValue.equals("")) {
                    attentionRequiredTowardsUsernameField.setAlpha(1);
                    proceedingNextFlag = false;
                } else {
                    attentionRequiredTowardsPasswordTypeField.setAlpha(0);
                }
                if (passwordValue.equals("")) {
                    attentionRequiredTowardsPasswordTypeField.setAlpha(1);
                    proceedingNextFlag = false;
                } else {
                    attentionRequiredTowardsPasswordTypeField.setAlpha(0);
                }
                if(proceedingNextFlag){
                    //proceed further
                    startActivity(new Intent(StudentLogin.this, MainActivity.class));
                }
            }
        }));


    }
}
