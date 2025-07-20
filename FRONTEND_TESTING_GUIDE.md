# Frontend-Backend Integration Testing Guide

## 🚀 Current Status

✅ **Backend (Django)**: Running on http://127.0.0.1:8000
✅ **CORS Configuration**: Properly configured for frontend communication
✅ **API Endpoints**: All working correctly
🔄 **Frontend (React)**: Starting up on http://localhost:3000

## 📋 How to Test Your Frontend

### 1. **Start Both Servers**

Make sure both servers are running:

```bash
# Terminal 1 - Django Backend (should already be running)
python manage.py runserver

# Terminal 2 - React Frontend
cd frontend
npm start
```

### 2. **Access Your Application**

Open your browser and go to: **http://localhost:3000**

### 3. **Test the Features**

#### ✅ **Authentication**
- Click "Signup" to create a new account
- Click "Login" to sign in with existing credentials
- Verify that the user info appears in the header after login

#### ✅ **Blog Posts**
- Check if posts are loading from the backend
- Verify post titles, content, and metadata are displayed
- Test the "Like" and "Comment" buttons (functionality can be added later)

#### ✅ **Categories**
- Check if categories are loading in the sidebar
- Verify category names are displayed correctly

#### ✅ **API Communication**
- Open browser DevTools (F12)
- Go to Network tab
- Refresh the page
- Verify that API calls to `/posts/` and `/categories/` are successful

### 4. **Troubleshooting**

#### If Frontend Shows "Failed to fetch posts":
1. Check that Django backend is running on port 8000
2. Verify CORS settings in `blogproject/settings.py`
3. Check browser console for CORS errors

#### If Frontend Won't Start:
1. Make sure you're in the `frontend` directory
2. Run `npm install` to install dependencies
3. Run `npm start` to start the development server

#### If API Calls Fail:
1. Check that Django server is running: `http://127.0.0.1:8000`
2. Test API directly: `http://127.0.0.1:8000/posts/`
3. Verify CORS headers in browser DevTools

### 5. **Expected Behavior**

#### ✅ **Working Features:**
- Modern, responsive UI with gradient background
- Login/Signup modals
- Blog posts display with titles, content, and metadata
- Categories sidebar
- User authentication state management
- API communication with Django backend

#### 🔄 **Features to Add Later:**
- Post creation form
- Comment functionality
- Like/dislike system
- Category filtering
- Image upload handling
- User profile management

### 6. **API Endpoints Available**

Your frontend can access these endpoints:

- `GET /posts/` - List all posts
- `GET /categories/` - List all categories
- `POST /login/` - User login
- `POST /signup/` - User registration
- `GET /` - Root endpoint (shows posts)

### 7. **Development Workflow**

1. **Backend Changes**: Django server auto-reloads
2. **Frontend Changes**: React dev server auto-reloads
3. **API Testing**: Use browser DevTools or tools like Postman
4. **Database**: Access via Django admin at `http://127.0.0.1:8000/admin/`

### 8. **Next Steps**

1. **Add more features** to the frontend
2. **Implement post creation** form
3. **Add comment system** functionality
4. **Implement like/dislike** system
5. **Add user profile** management
6. **Deploy** to production

## 🎯 Success Criteria

Your frontend is working correctly if:

✅ You can access `http://localhost:3000`
✅ The page loads without errors
✅ Posts and categories are displayed
✅ Login/Signup modals work
✅ No CORS errors in browser console
✅ API calls are successful in Network tab

## 🆘 Need Help?

If you encounter issues:

1. Check browser console for errors
2. Verify both servers are running
3. Test API endpoints directly
4. Check CORS configuration
5. Restart both servers if needed

Your Django backend is working perfectly! The frontend should now be able to communicate with it seamlessly. 🎉 