package com.thethreemusketeers.terminal;

import com.android.volley.toolbox.Volley;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;

public class StudentLogin2 {

    EditText userId, passwordEditText;

    @Override
    protected  void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_student_login2);

        RequestQueue requestQueue = Volley.newRequestQueue(this);

        // FETCHING XML ELEMENTS
        userId = fin
    }

}
