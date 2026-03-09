"""
Project Euler Status Dialog.
Displays user profile information and banner from Project Euler.
"""
import os
import requests
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QFormLayout, QLineEdit, QMessageBox,
                            QGroupBox)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QUrl


class ProjectEulerStatusDialog(QDialog):
    """Dialog to display Project Euler user profile information and banner."""
    
    @staticmethod
    def show(parent):
        """Show the Project Euler Status dialog."""
        dialog = ProjectEulerStatusDialog(parent)
        dialog.exec()
    
    def __init__(self, parent=None):
        """Initialize the dialog."""
        super().__init__(parent)
        self.setWindowTitle("Project Euler Status")
        self.setMinimumWidth(600)
        self.setMinimumHeight(400)
        
        # Create layout
        layout = QVBoxLayout(self)
        
        # Username input
        username_layout = QHBoxLayout()
        username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        self.fetch_button = QPushButton("Fetch Profile")
        self.fetch_button.clicked.connect(self.fetch_profile)
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)
        username_layout.addWidget(self.fetch_button)
        layout.addLayout(username_layout)
        
        # Profile information section
        profile_group = QGroupBox("Profile Information")
        profile_layout = QFormLayout()
        
        self.username_value = QLabel("-")
        self.country_value = QLabel("-")  # Will keep the variable name but update the label text
        self.language_value = QLabel("-")
        self.solved_value = QLabel("-")
        self.level_value = QLabel("-")
        
        profile_layout.addRow("Username:", self.username_value)
        profile_layout.addRow("Location:", self.country_value)  # Changed from "Country:" to "Location:"
        profile_layout.addRow("Language:", self.language_value)
        profile_layout.addRow("Problems Solved:", self.solved_value)
        profile_layout.addRow("Level:", self.level_value)
        
        profile_group.setLayout(profile_layout)
        layout.addWidget(profile_group)
        
        # Banner section
        banner_group = QGroupBox("Profile Banner")
        banner_layout = QVBoxLayout()
        self.banner_label = QLabel("Enter a username and click 'Fetch Profile' to display the banner")
        self.banner_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.banner_image = QLabel()
        self.banner_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        banner_layout.addWidget(self.banner_label)
        banner_layout.addWidget(self.banner_image)
        banner_group.setLayout(banner_layout)
        layout.addWidget(banner_group)
        
        # API information
        api_info = QLabel("Data retrieved using the Project Euler API")
        api_info.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addWidget(api_info)
        
        # Close button
        button_layout = QHBoxLayout()
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        button_layout.addStretch()
        button_layout.addWidget(close_button)
        layout.addLayout(button_layout)
        
        # Set dialog to modal
        self.setModal(True)
    
    def fetch_profile(self):
        """Fetch the profile information from Project Euler."""
        username = self.username_input.text().strip()
        
        if not username:
            QMessageBox.warning(self, "Error", "Please enter a username")
            return
            
        try:
            # Fetch profile information in XML format
            xml_url = f"https://projecteuler.net/profile/{username}.xml"
            response = requests.get(xml_url, timeout=10)
            
            if response.status_code == 200:
                # Check for empty response (indicates user doesn't exist)
                if not response.text.strip():
                    QMessageBox.warning(self, "Error", f"User '{username}' does not exist. (Empty response)")
                    print(f"Empty response for user: {username}")
                    return
                
                # Check if the response contains "does not exist" or other error indicator
                if "does not exist" in response.text.lower():
                    QMessageBox.warning(self, "Error", f"User '{username}' does not exist.")
                    print(f"User does not exist response: {response.text}")
                    return
                
                # Parse XML response
                import xml.etree.ElementTree as ET
                try:
                    root = ET.fromstring(response.text)
                except ET.ParseError:
                    # Check if we got HTML instead of XML (which happens when user doesn't exist)
                    if "<html" in response.text.lower():
                        QMessageBox.warning(self, "Error", 
                                          f"User '{username}' not found or the API returned an HTML page instead of XML.")
                        print("Got HTML instead of XML, likely user doesn't exist")
                        return
                    raise  # Re-raise if it's some other XML parsing error
                
                # Extract profile information with safe access - using correct field names
                username_elem = root.find("username")
                location_elem = root.find("location")  # API uses 'location' not 'country'
                language_elem = root.find("language")
                solved_elem = root.find("solved")
                level_elem = root.find("level")
                
                # Check if all required elements exist
                if None in [username_elem, location_elem, language_elem, solved_elem, level_elem]:
                    # Log the actual XML for debugging
                    print(f"Incomplete XML response: {response.text}")
                    
                    # Show error message
                    QMessageBox.warning(self, "Error", 
                                      "The profile data is incomplete or in an unexpected format.\n"
                                      "The user might not exist or the Project Euler API format may have changed.")
                    return
                
                # Safe access to text content
                username_value = username_elem.text
                location_value = location_elem.text  # Now using location instead of country
                language_value = language_elem.text
                solved_value = solved_elem.text
                level_value = level_elem.text
                
                # Handle special cases (like "Administrator")
                if solved_value and not solved_value.isdigit():
                    # Special value like "Administrator" - display as is
                    print(f"Special solved value for user {username}: {solved_value}")
                
                # Update profile information
                self.username_value.setText(username_value)
                self.country_value.setText(location_value)  # Display location in the country field
                self.language_value.setText(language_value)
                self.solved_value.setText(solved_value)
                self.level_value.setText(level_value)
                
                # Fetch and display banner
                self.fetch_banner(username)
                
                # Update banner label
                self.banner_label.setText(f"Profile banner for {username_value}")
            elif response.status_code == 404:
                QMessageBox.warning(self, "Error", f"User '{username}' not found. Please check the username and try again.")
            else:
                QMessageBox.warning(self, "Error", f"Failed to fetch profile: HTTP {response.status_code}")
                
        except ET.ParseError:
            QMessageBox.warning(self, "Error", "Failed to parse profile data. The response is not valid XML.")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to fetch profile: {str(e)}")
            print(f"Error fetching profile: {str(e)}")
    
    def fetch_banner(self, username):
        """Fetch and display the profile banner."""
        try:
            # Fetch profile banner
            banner_url = f"https://projecteuler.net/profile/{username}.png"
            response = requests.get(banner_url, timeout=10)
            
            if response.status_code == 200:
                # Check if the content is actually an image
                content_type = response.headers.get('Content-Type', '')
                if not content_type.startswith('image/'):
                    print(f"Warning: Received non-image content type: {content_type}")
                    self.banner_image.clear()
                    self.banner_label.setText("Banner not available (received non-image content)")
                    return
                
                # Create a temporary file to store the banner
                temp_path = os.path.join(os.path.dirname(__file__), "temp_banner.png")
                with open(temp_path, "wb") as f:
                    f.write(response.content)
                
                # Check if the file is valid
                pixmap = QPixmap(temp_path)
                if pixmap.isNull():
                    print(f"Warning: Invalid image data received for {username}")
                    self.banner_image.clear()
                    self.banner_label.setText("Invalid banner image received")
                else:
                    # Display the banner
                    self.banner_image.setPixmap(pixmap)
                    self.banner_label.setText(f"Profile banner for {username}")
                
                # Remove the temporary file
                try:
                    os.remove(temp_path)
                except Exception as e:
                    print(f"Warning: Failed to remove temporary file: {str(e)}")
            elif response.status_code == 404:
                self.banner_image.clear()
                self.banner_label.setText(f"Banner not found for user '{username}'")
            else:
                self.banner_image.clear()
                self.banner_label.setText(f"Failed to fetch banner: HTTP {response.status_code}")
                print(f"Failed to fetch banner: HTTP {response.status_code}")
                
        except Exception as e:
            self.banner_image.clear()
            self.banner_label.setText(f"Error: {str(e)}")
            print(f"Error fetching banner: {str(e)}") 