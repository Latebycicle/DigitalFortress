# Digital Fortress Escape Room

A cybersecurity-themed escape room experience that simulates a corporate network environment. Participants must find hidden clues, solve puzzles, and identify security vulnerabilities to complete the challenge.

## Components

This escape room consists of several interconnected components:

1. **Email System**: A realistic email client with phishing emails and important clues
2. **Company Website**: The Digital Fortress corporate website with hidden credentials
3. **File Upload Portal**: A secure file upload system that requires specific files to unlock a clue
4. **Server Backend**: Python server that powers the email system and other components

## Features

- **Realistic Corporate Environment**: Simulates a real company network with multiple interfaces
- **Educational Security Challenges**: Teaches participants about common security issues like:
  - Password exposure in source code comments
  - Phishing email identification
  - Suspicious file detection
  - Network credential discovery
- **Multiple Puzzle Elements**: Various challenges that require different skills to solve
- **Easy Setup**: Simple Python server that runs on any computer with minimal configuration

## Setup Instructions

### Server Setup

1. Clone this repository to your computer
2. Make sure you have Python 3 installed
3. Run the server script:
   ```
   python server.py
   ```
4. The server will start on port 8000 by default
5. All components will be accessible at `http://YOUR_LOCAL_IP:8000`

### Using a Different Port

If port 8000 is already in use, the server will automatically try to find an available port. You can also specify a custom port:

```
python server.py 8080
```

### Troubleshooting Port Issues

If you're having trouble with "Address already in use" errors, you can use the included script to kill processes using the port:

```
python kill_server.py
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

## Puzzle Solutions

This repository includes the necessary files for solving the puzzles:

- The `sus` directory contains files that participants need to discover
- The `sus/answer` directory contains the specific files needed for the upload portal challenge

## Customization

You can customize this escape room by:

1. Modifying the `emails.json` file to change or add emails
2. Editing the HTML files to change the appearance or content
3. Adding new challenges by creating additional HTML pages
4. Changing the hidden credentials in the HTML comments

## Browser Compatibility

This escape room works best on modern browsers (Chrome, Firefox, Safari, Edge).

## License

This project is available for personal and educational use. Feel free to modify and adapt it for your own escape room experiences.

## Acknowledgments

- Created for educational purposes to teach cybersecurity awareness
- Inspired by real-world security challenges and phishing techniques 