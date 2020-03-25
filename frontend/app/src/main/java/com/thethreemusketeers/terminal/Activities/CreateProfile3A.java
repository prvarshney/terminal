package com.thethreemusketeers.terminal.Activities;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.provider.MediaStore;
import android.view.View;
import android.widget.ImageView;

import com.thethreemusketeers.terminal.R;

public class CreateProfile3A extends AppCompatActivity {

    ImageView uploadBtn, deleteBtn, previewImageView;
    final int GALLERY_REQUEST_CODE = 1000;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_create_profile3a);

        // FETCHING ELEMENTS FROM XML DESIGN
        uploadBtn = findViewById(R.id.image_upload_btn);
        deleteBtn = findViewById(R.id.image_remove_btn);
        previewImageView = findViewById(R.id.attach_avatar);

        uploadBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent( Intent.ACTION_PICK ,MediaStore.Images.Media.EXTERNAL_CONTENT_URI );
                startActivityForResult(intent,GALLERY_REQUEST_CODE);
            }
        });

        deleteBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                previewImageView.setImageResource( R.drawable.ic_idcard_image);
            }
        });
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if ( requestCode == GALLERY_REQUEST_CODE && resultCode == RESULT_OK ) {
            previewImageView.setImageURI(data.getData());
        }
    }
}
