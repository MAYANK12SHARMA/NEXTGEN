css= '''
<style>
    .chat-message {
        padding: 1rem; /* Reduce padding */
        border-radius: 0.5rem; 
        margin-bottom: 0.5rem; /* Reduce margin */
        display: flex;
    }
    .chat-message.user {
        background-color: #2b313e;
    }
    .chat-message.bot {
        background-color: #475063;
    }
    .st-emotion-cache-7tauuy{
        padding-top: 1.5rem !important;
    }
    .chat-message .avatar {
        width: 15%; /* Reduce avatar width */
        display: flex; 
        align-items: center; /* Align avatar vertically */
        justify-content: center; /* Align avatar horizontally */
    }
    .chat-message .avatar img {
        max-width: 40px; /* Reduce image size */
        max-height: 40px; /* Reduce image size */
        border-radius: 50%;
        object-fit: cover;
    }
    .chat-message .message {
        width: 85%; /* Adjust width for message */
        padding-left: 0.5rem;
        color: #fff;
        display: flex;
        align-items: center; /* Center-align text vertically */
    }
    .css-18e3th9, 
    .css-1d391kg, 
    .st-emotion-cache-13ln4jf, 
    .st-emotion-cache-kgpedg {
        padding-top: 0 !important; /* Remove padding */
        padding-bottom: 0 !important; /* Remove padding */
    }
    .st-emotion-cache-1jicfl2, 
    .st-emotion-cache-7tauuy {
        padding-top: 0.5rem !important; /* Reduce padding for specific elements */
    }
    .css-18e3th9 {
            padding-top: 0 !important;
        }
        .css-1d391kg {
            padding-top: 0 !important;
        }
        .st-emotion-cache-13ln4jf{
            padding-top: 0 !important;
        }
        .st-emotion-cache-1jicfl2{
            padding-top: 1rem !important;
        }
        .st-emotion-cache-kgpedg{
            padding: 0 !important;
        }
        .st-emotion-cache-7tauuy{
            padding-top: 1rem !important;
        }
        
    #header {
        visibility: hidden;
    }
    </style>

'''
bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://i.ibb.co/cN0nmSj/Screenshot-2023-05-28-at-02-37-21.png" style="max-height: 50px; max-width: 50px; border-radius: 50%; object-fit: cover;">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
    <div class="chat-message user">
        <div class="avatar">
            <img src="https://img.freepik.com/premium-photo/animator-digital-avatar-generative-ai_934475-9312.jpg" style="max-height: 50px; max-width: 50px; border-radius: 50%; object-fit: cover;">
        </div>    
        <div class="message">{{MSG}}</div>
    </div>
'''
