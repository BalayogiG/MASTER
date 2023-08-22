package com.example.master;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.provider.Settings;
import android.widget.Button;
import android.widget.TextView;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;
import com.google.zxing.integration.android.IntentIntegrator;
import com.google.zxing.integration.android.IntentResult;

import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.biometric.BiometricManager;
import androidx.biometric.BiometricPrompt;
import androidx.core.content.ContextCompat;
import androidx.fragment.app.FragmentActivity;

import org.json.JSONException;
import org.json.JSONObject;


public class RegisterAssist extends AppCompatActivity {

    Button btnScanToConfirm;
    TextView txtUsername;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_register_assist);

        AuthenticateFingerPrint();
        txtUsername = findViewById(R.id.username);
        btnScanToConfirm = findViewById(R.id.btnReg);
        btnScanToConfirm.setOnClickListener(view -> {
            IntentIntegrator intentIntegrator = new IntentIntegrator(this);
            intentIntegrator.setPrompt("Scan QR code to Confirm Registration");
            intentIntegrator.setOrientationLocked(true);
            intentIntegrator.initiateScan();
        });
    }

    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        IntentResult intentResult = IntentIntegrator.parseActivityResult(requestCode, resultCode, data);
        // if the intentResult is null then
        // toast a message as "cancelled"
        if (intentResult != null) {
            if (intentResult.getContents() == null) {
                Toast.makeText(getBaseContext(), "Cancelled", Toast.LENGTH_SHORT).show();
            } else {
                // if the intentResult is not null we'll set
                // the content and format of scan message
                String msg = intentResult.getContents();
                String username = txtUsername.getText().toString();
                String sec_id = Settings.Secure.getString(this.getContentResolver(), Settings.Secure.ANDROID_ID);
                Intent intent = getIntent();
                String url = intent.getStringExtra("url");
                String userdata = username + "$" + sec_id;
                PostMessage(userdata, url);
            }
        } else {
            super.onActivityResult(requestCode, resultCode, data);
        }
    }

    private void PostMessage(String originalString, String url) {
        // Create JSON object to send to the server
        JSONObject jsonObject = new JSONObject();
        try {
            jsonObject.put("message", originalString);
        } catch (JSONException e) {
            e.printStackTrace();
        }

        // Create a new Volley request queue
        RequestQueue requestQueue = Volley.newRequestQueue(this);

        // Create a POST request with the JSON object
        JsonObjectRequest jsonObjectRequest = new JsonObjectRequest(Request.Method.POST, url, jsonObject,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        // Handle the response from the server
//                        Log.d(TAG, "Server response: " + response.toString());
                        Toast.makeText(RegisterAssist.this, response.toString(), Toast.LENGTH_SHORT).show();
                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        // Handle the error response
                        if (error.networkResponse != null && error.networkResponse.data != null) {
                            try {
                                // Attempt to parse the error response as a JSONObject
                                String errorResponse = new String(error.networkResponse.data);
                                JSONObject jsonObject = new JSONObject(errorResponse);
//                                Log.e(TAG, "Error response: " + jsonObject.toString());
                            } catch (JSONException e) {
                                // Handle the case when the error response is not in JSON format
//                                Log.e(TAG, "Error response: " + new String(error.networkResponse.data));
                            }
                        } else {
//                            Log.e(TAG, "Error: " + error.toString());
                        }
                    }
                });

        // Add the request to the request queue
        requestQueue.add(jsonObjectRequest);
        txtUsername.setText("");
    }

    private void AuthenticateFingerPrint() {
        switch (BiometricManager.from(this).canAuthenticate()){
            case 0:
                Toast.makeText(this, "You can use the fingerprint sensor to login", Toast.LENGTH_SHORT).show();
                break;
            case 1:
                Toast.makeText(this, "The biometric sensor is currently unavailable", Toast.LENGTH_SHORT).show();
                break;
            case 11:
                Toast.makeText(this, "Your device doesn't have fingerprint saved,please check your security settings", Toast.LENGTH_SHORT).show();
                break;
            case 12:
                Toast.makeText(this, "This device does not have a fingerprint sensor", Toast.LENGTH_SHORT).show();
                break;
        } new BiometricPrompt((FragmentActivity) this, ContextCompat.getMainExecutor(this), (BiometricPrompt.AuthenticationCallback) new BiometricPrompt.AuthenticationCallback(){
            @Override
            public void onAuthenticationError(int errorCode, @NonNull CharSequence errString) {
                super.onAuthenticationError(errorCode, errString);
            }

            @Override
            public void onAuthenticationSucceeded(@NonNull BiometricPrompt.AuthenticationResult result) {
                super.onAuthenticationSucceeded(result);
                Toast.makeText(RegisterAssist.this.getApplicationContext(), "Fingerprint Authentication Success", Toast.LENGTH_SHORT).show();
            }

            @Override
            public void onAuthenticationFailed() {
                super.onAuthenticationFailed();
            }
        }).authenticate(new BiometricPrompt.PromptInfo.Builder().setTitle("MASTER Fingerprint").setDescription("Use your fingerprint to authenticate").setNegativeButtonText("Cancel").build());
    }
}