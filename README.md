# Digital Fortress Escape Room

Digital Fortress escape was an Escape room conducted during FOOBAR 9.0 (An ASCII event under the Department of Computer Science and Engineering, Christ University Kengeri Campus). 

## Components

This escape room consists of several interconnected components:

1. **Email System**: A realistic email client with phishing emails and important clues
2. **Company Website**: The Digital Fortress corporate website with hidden credentials
3. **File Upload Portal**: A file upload system that requires specific files to unlock a clue
4. **Server Backend**: Python server that powers the email system and other components
5. *Media*: An adobe Illustrator file with all of the material used for the escape room

These components are hosted on a LAN and are available to access to any computers that are connected to the Local Area Network

## Storyline

You applied for a job at DigitalFortress, a shady cybersecurity company. You've gotten through the first two rounds of interviews and they invite you to an abandoned warehouse for the final round of the interview. Once you're there, You're locked in the warehouse and escaping the warehouse is the final round of the interview. 


## Setup Instructions

### Server Setup

1. Clone this repository to your computer
2. Make sure you have Python 3 installed
3. Run the server script:
   ```
   python server.py
   ```
4. The server will start on port 8000 by default
5. All components will be accessible at `http://YOUR_LOCAL_IP:8000` and `localhost:8000` 

### Using a Different Port

If port 8000 is already in use, the server will automatically try to find an available port. You can also specify a custom port:

```
python server.py 8080
```


## Escape Room Components

### Email System

The email system includes:
- **User Interface**: A clean, modern email client interface
- **Admin Panel**: For setting up and managing emails
- **Phishing Emails**: Pre-configured suspicious emails with clues
- **Official Communications**: Company emails with important information

Participants can access:
- Email client: `http://YOUR_LOCAL_IP:8000/index.html`

Game masters can access:
- Admin panel: `http://YOUR_LOCAL_IP:8000/admin.html`

### Company Website

The Digital Fortress company website contains:
- Information about the fictional cybersecurity company
- Hidden credentials in HTML comments
- Security announcements with subtle hints

Access at: `http://YOUR_LOCAL_IP:8000/company.html`

### File Upload Portal

A secure file upload system that:
- Requires participants to find and upload specific files
- Provides feedback on verification attempts
- Supports drag-and-drop functionality
- Reveals a clue when the correct files are uploaded

Access at: `http://YOUR_LOCAL_IP:8000/upload.html`


## Browser Compatibility

This escape room works best on modern browsers (Chrome, Firefox, Safari, Edge).


## Acknowledgments

- Created for educational purposes to teach cybersecurity awareness
- Inspired by real-world security challenges and phishing techniques 