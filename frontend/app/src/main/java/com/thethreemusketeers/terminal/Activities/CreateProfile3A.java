package com.thethreemusketeers.terminal.Activities;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.os.Bundle;
import android.provider.MediaStore;
import android.util.Base64;
import android.util.Log;
import android.view.View;
import android.widget.ImageView;

import com.thethreemusketeers.terminal.JSONRequestObject.UserRegisterObject;
import com.thethreemusketeers.terminal.R;

import java.io.ByteArrayOutputStream;
import java.io.FileNotFoundException;
import java.io.InputStream;
import java.net.URI;

public class CreateProfile3A extends AppCompatActivity {

    ImageView uploadBtn, deleteBtn, previewImageView;
    View nextBtn;
    String base64EncImage;
    final int GALLERY_REQUEST_CODE = 1000;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_create_profile3a);

        // FETCHING ELEMENTS FROM XML DESIGN
        uploadBtn = findViewById(R.id.image_upload_btn);
        deleteBtn = findViewById(R.id.image_remove_btn);
        previewImageView = findViewById(R.id.attach_avatar);
        nextBtn = findViewById(R.id.activity3a_next_btn);

        // SETTING EVENT LISTENER ON UPLOAD BUTTON, WHENEVER IT GETS CLICKED IT OPENS A NEW INTENT
        // TO SELECT IMAGE FROM MEDIA STORE
        uploadBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent( Intent.ACTION_PICK ,MediaStore.Images.Media.EXTERNAL_CONTENT_URI );
                startActivityForResult(intent,GALLERY_REQUEST_CODE);
            }
        });

        // SETTING EVENT LISTENER ON DELETE BUTTON, WHENEVER IT GETS CLICKED IT REPLACE THE PREVIEW
        // IMAGE WITH DEFAULT ONE AND REPLACES base64EncImage WITH NULL STRING
        deleteBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                previewImageView.setImageResource( R.drawable.ic_idcard_image);
                base64EncImage = null;
            }
        });

        // SETTING EVENT LISTENER ON NEXT BUTTON, WHENEVER IT GETS CLICKED ITS STYLE CHANGES TO PROGRESSING
        // STATE TILL IT DOESN'T SENDS IMAGE TO THE SERVER AS BASE64 ENCODED STRING
        nextBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                UserRegisterObject.image = base64EncImage;
                startActivity(new Intent(CreateProfile3A.this,CreateProfile4.class));
            }
        });
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if ( requestCode == GALLERY_REQUEST_CODE && resultCode == RESULT_OK ) {
            // FETCHING IMAGE URI OF SELECTED FILE
            final Uri imageURI = data.getData();
            // CHANGING FILE AVATAR WITH SELECTED FILE IMAGE
            previewImageView.setImageURI( imageURI );
            // GETTING IMAGE FILE IN INPUT STREAM
            InputStream inputStream = null;
            try {
                inputStream = getContentResolver().openInputStream(imageURI);
            } catch (FileNotFoundException e) {
                e.printStackTrace();
            }
            // CONVERTING IMAGE FROM INPUT STREAM TO BITMAP IMAGE
            Bitmap bmp = BitmapFactory.decodeStream(inputStream);
            ByteArrayOutputStream baos = new ByteArrayOutputStream();
            bmp.compress(Bitmap.CompressFormat.JPEG,100,baos);
            byte[] byteArr = baos.toByteArray();
            base64EncImage = Base64.encodeToString(byteArr, Base64.DEFAULT);

        }
    }
}
