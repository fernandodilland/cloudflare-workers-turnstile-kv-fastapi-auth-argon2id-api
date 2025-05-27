use serde::Deserialize;
use worker::*;

#[derive(Deserialize)]
struct TurnstileVerifyResponse {
    success: bool,
    #[serde(rename = "error-codes")]
    error_codes: Option<Vec<String>>,
}

pub async fn verify_turnstile_token(token: &str, secret: &str) -> std::result::Result<(), Box<dyn std::error::Error>> {
    let mut init = RequestInit::new();
    init.method = Method::Post;
    
    // Create form data for Turnstile verification
    let form_data = format!("secret={}&response={}", secret, token);
    init.body = Some(form_data.into());
    
    // Set content type header for form data
    let mut headers = Headers::new();
    headers.set("Content-Type", "application/x-www-form-urlencoded")?;
    init.headers = headers;

    let request = Request::new_with_init("https://challenges.cloudflare.com/turnstile/v0/siteverify", &init)?;
    
    let mut response = Fetch::Request(request).send().await?;
    let verify_response: TurnstileVerifyResponse = response.json().await?;

    if verify_response.success {
        Ok(())
    } else {
        Err("Turnstile verification failed".into())
    }
}
