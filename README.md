<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>🏨 Room Booking API - README</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; padding: 20px; background: #f9f9f9; color: #333; }
        h2, h3, h4 { color: #1f4e79; }
        code { background: #eee; padding: 2px 6px; border-radius: 4px; font-family: monospace; }
        pre { background: #eee; padding: 10px; border-radius: 5px; overflow-x: auto; }
        a { color: #1f4e79; text-decoration: none; }
        a:hover { text-decoration: underline; }
        ul { margin-top: 0; }
    </style>
</head>
<body>

<h2>🏨 Room Booking API</h2>

<p>
    The <strong>Room Booking API</strong> is a Django REST Framework-based backend system
    for managing room reservations. It allows users to view available rooms, book rooms,
    manage their bookings, and interact with the system through secure API endpoints. 🛏️
</p>

<h2>📌 Project Overview</h2>
<p>
    This API is designed to handle room bookings in a structured, scalable manner.
    It includes models for <strong>Rooms</strong>, <strong>Users</strong>, <strong>Occupied Dates</strong>,
    and <strong>Room Images</strong>. The API supports authentication, authorization,
    and role-based access control to separate regular users and administrators. 🧑‍💻
</p>

<h2>💻 System Requirements</h2>
<ul>
    <li>🐍 Python 3.10+</li>
    <li>🕸️ Django 6.0+</li>
    <li>🧩 Django REST Framework</li>
    <li>🗄️ SQLite (default) or another relational database</li>
    <li>🔧 Optional: Postman or any API testing client</li>
</ul>

<h2>⚙️ Installation & Setup</h2>
<ol>
    <li>Clone the repository:  
    <pre><code>git clone https://github.com/yourusername/room-booking-api.git</code></pre></li>

    <li>Navigate to the project folder:  
    <pre><code>cd room-booking-api</code></pre></li>

    <li>Create and activate a virtual environment:  
    <pre><code>python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows</code></pre></li>

    <li>Install dependencies:  
    <pre><code>pip install -r requirements.txt</code></pre></li>

    <li>Apply database migrations:  
    <pre><code>python manage.py migrate</code></pre></li>

    <li>Create a superuser for admin access:  
    <pre><code>python manage.py createsuperuser</code></pre></li>

    <li>Run the development server:  
    <pre><code>python manage.py runserver</code></pre></li>
</ol>

<h2>📂 Models</h2>
<p>
    The application contains the following main models:
</p>
<ul>
    <li>🏢 <strong>Room:</strong> Represents hotel rooms. Contains type, price, occupancy, and description.</li>
    <li>🖼️ <strong>RoomImage:</strong> Stores images related to rooms with optional captions.</li>
    <li>📅 <strong>OccupiedDate:</strong> Tracks which user has booked which room on which date, enforcing uniqueness to prevent double bookings.</li>
    <li>👤 <strong>User:</strong> Custom user model based on email authentication with a full_name field.</li>
</ul>

<h2>🛠️ Serializers</h2>
<p>
    Serializers convert model instances into JSON data for API responses and validate incoming data:
</p>
<ul>
    <li>📦 <strong>RoomSerializer:</strong> Includes room details, related images, and occupied dates.</li>
    <li>📅 <strong>OccupiedDateSerializer:</strong> Manages bookings, linking users and rooms.</li>
    <li>🖼️ <strong>RoomImageSerializer:</strong> Handles room images and captions.</li>
    <li>👤 <strong>UserSerializer:</strong> Handles user creation, including password hashing and validation.</li>
</ul>

<h2>📝 Views & API Endpoints</h2>
<p>
    The API uses Django REST Framework views to manage endpoints:
</p>
<ul>
    <li>🛏️ <strong>RoomList & RoomDetail:</strong> Admin-only views for creating, updating, and deleting rooms.</li>
    <li>📅 <strong>OccupiedDatesList & OccupiedDatesDetail:</strong> Manage bookings; users see only their bookings, while staff can access all.</li>
    <li>👤 <strong>UserList & UserDetail:</strong> Expose user data with permission checks.</li>
    <li>🔑 <strong>Register & Login:</strong> Handle user registration and token-based authentication.</li>
</ul>

<h2>🔐 Authentication & Permissions</h2>
<ul>
    <li>✉️ Custom <code>EmailBackend</code> allows login via email instead of username.</li>
    <li>🔑 Token-based authentication for API access.</li>
    <li>🛡️ Permissions control access:
        <ul>
            <li>📝 <code>IsOwnerOrReadOnly</code> ensures users can modify only their own bookings.</li>
            <li>👑 <code>IsAdminOrReadOnly</code> allows admins full control while others can only read.</li>
        </ul>
    </li>
</ul>

<h2>🌐 URL Routing</h2>
<p>
    URL paths follow REST conventions:
</p>
<ul>
    <li><code>/rooms/</code> - List and create rooms</li>
    <li><code>/rooms/&lt;id&gt;/</code> - Retrieve, update, delete a room</li>
    <li><code>/occupied-dates/</code> - List and create bookings</li>
    <li><code>/occupied-dates/&lt;id&gt;/</code> - Manage a specific booking</li>
    <li><code>/users/</code> - List users (admin-only)</li>
    <li><code>/users/&lt;id&gt;/</code> - Retrieve user profile</li>
    <li><code>/login/</code> - Obtain token via credentials</li>
    <li><code>/register/</code> - Create new user and token</li>
</ul>

<h2>🧪 Testing & Error Handling</h2>
<ul>
    <li>⚠️ API endpoints handle invalid requests gracefully using DRF exceptions.</li>
    <li>🔒 Permissions and ownership checks prevent unauthorized access.</li>
    <li>📅 Edge cases like double bookings or exceeding max occupancy are validated at the model and serializer level.</li>
    <li>📝 Logs and responses provide clear error messages to clients.</li>
</ul>

<h2>💡 Reflections & Learning</h2>
<p>
    Building this API highlighted key Django and REST concepts:
</p>
<ul>
    <li>🛠️ Understanding the ORM and model relationships is crucial for reliable data handling.</li>
    <li>🔄 Serializers act as a bridge between models and API clients, enabling validation and nested data management.</li>
    <li>🛣️ Views and URL routing enforce clean API architecture and permission logic.</li>
    <li>🔑 Authentication and token-based security are essential for protecting user data.</li>
</ul>

<h2>🚀 Future Enhancements</h2>
<ul>
    <li>🔍 Add search and filtering for rooms by type, price, or availability.</li>
    <li>📆 Integrate calendar views for bookings.</li>
    <li>✉️ Add email notifications for booking confirmations.</li>
    <li>🛡️ Implement rate limiting and advanced security measures for production.</li>
</ul>

<p><strong>Author:</strong> Tobias Kibichii</p>
<p><strong>License:</strong> MIT</p>

</body>
</html>
