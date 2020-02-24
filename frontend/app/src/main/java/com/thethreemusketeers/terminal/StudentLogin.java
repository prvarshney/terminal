package com.thethreemusketeers.terminal;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.text.method.PasswordTransformationMethod;
import android.view.View;
import android.widget.EditText;
import android.widget.ImageView;

public class StudentLogin extends AppCompatActivity {

    EditText passwordEditText;
    ImageView passwordEye;
    Boolean eyeTogglerFlag = true;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_student_login);

        passwordEditText = findViewById(R.id.password_edit_text);
        passwordEye = findViewById(R.id.password_eye);

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


    }
}
