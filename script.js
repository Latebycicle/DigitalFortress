document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const emailList = document.querySelector('.email-list');
    const emailSubject = document.getElementById('email-subject');
    const emailFrom = document.getElementById('email-from');
    const emailTimestamp = document.getElementById('email-timestamp');
    const emailBody = document.getElementById('email-body');

    // Load emails from server on page load
    loadEmails();

    // Set up auto-refresh every 30 seconds
    setInterval(loadEmails, 30000);

    // Functions
    async function loadEmails() {
        try {
            console.log("Attempting to fetch emails from server...");
            
            // Fetch emails from server with timeout
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 5000); // 5 second timeout
            
            const response = await fetch('/api/emails', { 
                signal: controller.signal,
                cache: 'no-store' // Prevent caching issues
            });
            
            clearTimeout(timeoutId);
            
            if (!response.ok) {
                throw new Error(`Server returned ${response.status}: ${response.statusText}`);
            }
            
            const emails = await response.json();
            console.log(`Successfully loaded ${emails.length} emails`);
            
            // Clear current email list
            emailList.innerHTML = '';
            
            if (!emails || emails.length === 0) {
                const emptyState = document.createElement('div');
                emptyState.className = 'email-item';
                emptyState.innerHTML = '<p class="placeholder">No emails available</p>';
                emailList.appendChild(emptyState);
                return;
            }
            
            // Sort emails by timestamp (newest first)
            emails.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
            
            // Add each email to the list
            emails.forEach(email => {
                const emailItem = document.createElement('div');
                emailItem.className = 'email-item';
                emailItem.dataset.id = email.id;
                
                // Format the timestamp
                const date = new Date(email.timestamp);
                const formattedDate = formatDate(date);
                
                emailItem.innerHTML = `
                    <h3>${email.subject}</h3>
                    <p>From: ${email.from}</p>
                    <div class="timestamp">${formattedDate}</div>
                `;
                
                emailItem.addEventListener('click', function() {
                    // Remove selected class from all emails
                    document.querySelectorAll('.email-item').forEach(item => item.classList.remove('selected'));
                    
                    // Add selected class to this email
                    this.classList.add('selected');
                    
                    // Display email content
                    displayEmail(email);
                });
                
                emailList.appendChild(emailItem);
            });
            
            // Select and display the first email
            if (emails.length > 0) {
                const firstEmail = emailList.querySelector('.email-item');
                firstEmail.classList.add('selected');
                displayEmail(emails[0]);
            }
        } catch (error) {
            console.error('Error loading emails:', error);
            
            let errorMessage = 'Error loading emails. Please try again later.';
            
            // More specific error messages based on the error type
            if (error.name === 'AbortError') {
                errorMessage = 'Request timed out. Server may be unavailable.';
            } else if (error.message.includes('Failed to fetch')) {
                errorMessage = 'Could not connect to server. Check your network connection.';
            } else if (error.message.includes('JSON')) {
                errorMessage = 'Invalid data received from server.';
            }
            
            emailList.innerHTML = `<div class="email-item"><p class="placeholder">${errorMessage}</p></div>`;
            
            // Clear email content area when there's an error
            emailSubject.textContent = 'No email selected';
            emailFrom.textContent = '';
            emailTimestamp.textContent = '';
            emailBody.innerHTML = '<p class="placeholder">No email selected</p>';
        }
    }

    function displayEmail(email) {
        try {
            // Set email details
            emailSubject.textContent = email.subject;
            emailFrom.textContent = `From: ${email.from}`;
            
            // Format and display timestamp
            const date = new Date(email.timestamp);
            emailTimestamp.textContent = formatDate(date);
            
            // Convert markdown to HTML for the content
            if (typeof marked !== 'undefined') {
                emailBody.innerHTML = marked.parse(email.content);
            } else {
                console.warn('Marked library not loaded, displaying plain text');
                emailBody.innerHTML = `<pre>${email.content}</pre>`;
            }
        } catch (error) {
            console.error('Error displaying email:', error);
            emailBody.innerHTML = '<p class="placeholder">Error displaying email content</p>';
        }
    }

    function formatDate(date) {
        try {
            const options = { 
                year: 'numeric', 
                month: 'short', 
                day: 'numeric', 
                hour: '2-digit', 
                minute: '2-digit' 
            };
            return date.toLocaleString('en-US', options);
        } catch (error) {
            console.error('Error formatting date:', error);
            return 'Unknown date';
        }
    }
}); 