document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const fromInput = document.getElementById('email-from-input');
    const subjectInput = document.getElementById('email-subject-input');
    const datetimeInput = document.getElementById('email-datetime-input');
    const contentInput = document.getElementById('email-content-input');
    const addEmailBtn = document.getElementById('add-email-btn');
    const clearEmailsBtn = document.getElementById('clear-emails-btn');
    const viewInboxBtn = document.getElementById('view-inbox-btn');
    const previewSubject = document.getElementById('preview-subject');
    const previewFrom = document.getElementById('preview-from');
    const previewTimestamp = document.getElementById('preview-timestamp');
    const previewBody = document.getElementById('preview-body');

    // Initialize the current date/time in the datetime input
    const now = new Date();
    datetimeInput.value = now.toISOString().substring(0, 16);

    // Event Listeners
    addEmailBtn.addEventListener('click', addEmail);
    clearEmailsBtn.addEventListener('click', clearEmails);
    viewInboxBtn.addEventListener('click', viewInbox);
    
    // Live preview for content
    contentInput.addEventListener('input', updatePreview);
    fromInput.addEventListener('input', updatePreview);
    subjectInput.addEventListener('input', updatePreview);
    datetimeInput.addEventListener('input', updatePreview);

    // Functions
    async function addEmail() {
        // Validate inputs
        if (!fromInput.value || !subjectInput.value || !contentInput.value || !datetimeInput.value) {
            alert('Please fill in all fields');
            return;
        }

        // Create email object
        const email = {
            id: Date.now(), // Use timestamp as unique ID
            from: fromInput.value,
            subject: subjectInput.value,
            timestamp: datetimeInput.value,
            content: contentInput.value
        };

        try {
            // Send email to server
            const response = await fetch('/api/emails', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(email)
            });
            
            const result = await response.json();
            
            if (result.success) {
                // Clear form
                fromInput.value = '';
                subjectInput.value = '';
                contentInput.value = '';
                
                // Reset datetime to current
                const now = new Date();
                datetimeInput.value = now.toISOString().substring(0, 16);
                
                // Update preview
                updatePreview();
                
                alert('Email added successfully!');
            } else {
                alert('Error adding email: ' + (result.error || 'Unknown error'));
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Error adding email. Please check the console for details.');
        }
    }

    async function clearEmails() {
        if (confirm('Are you sure you want to clear all emails? This cannot be undone.')) {
            try {
                const response = await fetch('/api/clear', {
                    method: 'POST'
                });
                
                const result = await response.json();
                
                if (result.success) {
                    alert('All emails have been cleared.');
                } else {
                    alert('Error clearing emails: ' + (result.error || 'Unknown error'));
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Error clearing emails. Please check the console for details.');
            }
        }
    }

    function viewInbox() {
        window.open('index.html', '_blank');
    }

    function updatePreview() {
        // Update preview with current form values
        previewSubject.textContent = subjectInput.value || 'Email Subject';
        previewFrom.textContent = `From: ${fromInput.value || 'sender@example.com'}`;
        
        // Format and display timestamp
        let date;
        if (datetimeInput.value) {
            date = new Date(datetimeInput.value);
        } else {
            date = new Date();
        }
        previewTimestamp.textContent = formatDate(date);
        
        // Convert markdown to HTML for the content
        if (contentInput.value) {
            previewBody.innerHTML = marked.parse(contentInput.value);
        } else {
            previewBody.innerHTML = '<p>Email content will appear here...</p>';
        }
    }

    function formatDate(date) {
        const options = { 
            year: 'numeric', 
            month: 'short', 
            day: 'numeric', 
            hour: '2-digit', 
            minute: '2-digit' 
        };
        return date.toLocaleString('en-US', options);
    }
    
    // Initialize preview
    updatePreview();
}); 