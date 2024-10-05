### Giraffe Notes
- Meta Info:
	- Prompt - I bet you can't access my notes on giraffes!
	- link - http://chal.competitivecyber.club:8081/
- The webpage has nothing on it besides some basic CSS & HTML body
- Look at the source code and at the top there's an interesting `if()` check:
	- ![attachments/Pasted image 20240924131501.png|500](attachments/Pasted%20image%2020240924131501.png)
- That `if()` check is used here:
	- ![attachments/Pasted image 20240924131530.png||500](attachments/Pasted%20image%2020240924131530.png)
	- with extra HTML elements including the flag being inside the `else()` statement
- So it's a basic `x-forwarded-for` vulnerability and the source file let's us know which IP-addresses have higher-level access
- Here's documentation on the [X-Forwarded-For HTTP Header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Forwarded-For)
- But essentially the XFF-Header lets a server know what the original IP address of the client connecting to it was, in case of there being proxies or other middle-men between transmissions
- So just open up Burpsuite  -->  paste in the challenge link in the burp-chromium-browser  -->  send to repeater  -->  and add in this line
	- `X-Forwarded-For: 127.0.0.1`
	- ![Pasted image 20241001113913.png](attachments/Pasted%20image%2020241001113913.png)
- Now the server will think you're the owner/admin of the page and give you the flag
- Flag: CACI{1_lik3_g1raff3s_4_l0t}

### Impersonate
- Meta Info:
	- prompt - one may not be who they say they are
	- link - http://chal.competitivecyber.club:9999/
- If you input any string with substring "admin" for the username it won't let you login
- if you input anything else it logs you in & creates a "session" cookie 
- `username: me` & `password: password`
	- example cookie = `eyJ1aWQiOiIzYmFlNjA1ZC1jZWNlLTU0NmItOTdhMC0xZTAxNDBlMWUzZTAiLCJ1c2VybmFtZSI6Im1lIn0.Zu7mZQ.1tbKyVzMtyezXdVATaHW8xs1J8s`
- The server prevents non-alphanumeric inputs for the "username" but not for the password
	- typical XSS payloads won't cause anything on our end
	- And even though there's templating here  ![attachments/Pasted image 20240921115435.png](attachments/Pasted%20image%2020240921115435.png)
	- no typical SSTI payloads do anything either so it's probably not XSS or SSTI
- Here are the requisites to be recognized as an admin and get the flag:
	- ![attachments/Pasted image 20240921134330.png||500](attachments/Pasted%20image%2020240921134330.png)
	- It only cares about the "session" cookie which has 3 parts: 
		- `is_admin` boolean, `uid` value, and a `username` value
- Parts of the Solution
	- Can decode the "session" cookie from Flask to know the formatting for any user(just login once)
		- ![attachments/Pasted image 20240921134045.png||300](attachments/Pasted%20image%2020240921134045.png)
		- used this [online flask session cookie decoder](https://www.kirsle.net/wizards/flask-session.cgi)
	- We have the "UUID" and can make the same instance of it as the server 
		- ![attachments/Pasted image 20240921135241.png||300](attachments/Pasted%20image%2020240921135241.png)
		- With the UUID we can make any `uid` we want
			- ![attachments/Pasted image 20240921135201.png||300](attachments/Pasted%20image%2020240921135201.png)
	- Need the Secure Key used to make/encrypt each session cookie which in this case is based off the server's start time
		- ![attachments/Pasted image 20240921134930.png||400](attachments/Pasted%20image%2020240921134930.png)
		- The server's start time periodically resets at intervals to prevent people from bruteforcing by just steadily going back in time so it only works for a certain breadth of time
		- Can reverse engineer the `server_start_time` from the `/status` page
		- ![attachments/Pasted image 20240921135034.png||350](attachments/Pasted%20image%2020240921135034.png)
- Whole Solution:
	1. Create the same "uid" as the administrator with `uid = uuid.uuid5(secret, 'administrator)`
	2. Get the server's start time to create the "secure_key"  by looking at the `/status`page
		- do "current time - uptime" to get `server_start_time`
	3. Create your own "administrator" session cookie
		- use this python script [flask_session_manager](https://github.com/noraj/flask-session-cookie-manager) to create cookies
	4. go to the `/admin`webpage after overwriting your default session cookie with the one made in step 3
- **Flag**: PCTF{Imp3rs0n4t10n_Iz_Sup3r_Ezz}


### Open Sesame (Incomplete)
- Meta Info:
	- http://chal.competitivecyber.club:13336/
	- Does the CLI listen to magic?
- In a reverse to the usual setup, we are giving the admin bot commands, but can't see the response from the server 
- can pass the bot pages to visit hosted by the server
- the flag is in `http://127.0.0.1:1337/api/cal` 
	- however admin bot disallows the substring "cal" & "%" from being used as input, so no URL encodings



