const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');

// Set up Express App
const app = express();
app.use(express.json());
app.use(cors());

// MongoDB Connection (Make sure to replace with your actual MongoDB URI)
const mongoURI = 'mongodb+srv://adnankstheredteamlabs:Adnan%4066202@cluster0.qrppz7h.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0';
mongoose.connect(mongoURI, {
    useNewUrlParser: true,
    useUnifiedTopology: true
})
.then(() => console.log('Connected to MongoDB Atlas'))
.catch(error => console.error('Error connecting to MongoDB:', error));

// Mongoose Schema and Models
const cadetSchema = new mongoose.Schema({
    cadetID: { type: String, required: true },
    name: { type: String, required: true },
    rank: { type: String, required: true },
    isPresent: { type: Boolean, default: false }
});

const eventSchema = new mongoose.Schema({
    eventName: { type: String, required: true },
    attendanceData: [cadetSchema],
    date: { type: Date, default: Date.now }
});

const blogSchema = new mongoose.Schema({
    title: { type: String, required: true },
    content: { type: String, required: true },
    date: { type: Date, default: Date.now }
});

const Event = mongoose.model('Event', eventSchema);
const Cadet = mongoose.model('Cadet', cadetSchema); // Cadet model for fetching data
const Blog = mongoose.model('Blog', blogSchema); // Blog model for managing blog posts

// Routes

// Create a New Event with Attendance Data
app.post('/api/events', async (req, res) => {
    try {
        const { eventName, attendanceData } = req.body;
        const newEvent = new Event({ eventName, attendanceData });
        await newEvent.save();
        res.status(201).json({ message: 'Attendance data saved successfully' });
    } catch (error) {
        res.status(500).json({ message: 'Error saving attendance data', error });
    }
});

// Get All Events
app.get('/api/events', async (req, res) => {
    try {
        const events = await Event.find();
        res.json(events);
    } catch (error) {
        res.status(500).json({ message: 'Error fetching events', error });
    }
});

// Get All Cadets
app.get('/api/cadets', async (req, res) => {
    try {
        const cadets = await Cadet.find();
        res.json(cadets);
    } catch (error) {
        res.status(500).json({ message: 'Error fetching cadets', error });
    }
});

// Add a New Cadet
app.post('/api/cadets', async (req, res) => {
    try {
        const { cadetID, name, rank, isPresent } = req.body;
        const newCadet = new Cadet({ cadetID, name, rank, isPresent });
        await newCadet.save();
        res.status(201).json({ message: 'Cadet added successfully', cadet: newCadet });
    } catch (error) {
        res.status(500).json({ message: 'Error adding cadet', error });
    }
});

// Get a Cadet by ID
app.get('/api/cadets/:id', async (req, res) => {
    try {
        const cadet = await Cadet.findById(req.params.id);
        if (!cadet) return res.status(404).json({ message: 'Cadet not found' });
        res.json(cadet);
    } catch (error) {
        res.status(500).json({ message: 'Error fetching cadet', error });
    }
});

// Update a Cadet by ID
app.put('/api/cadets/:id', async (req, res) => {
    try {
        const { cadetID, name, rank, isPresent } = req.body;
        const cadet = await Cadet.findByIdAndUpdate(req.params.id, { cadetID, name, rank, isPresent }, { new: true });
        if (!cadet) return res.status(404).json({ message: 'Cadet not found' });
        res.json(cadet);
    } catch (error) {
        res.status(500).json({ message: 'Error updating cadet', error });
    }
});

// Delete a Cadet by ID
app.delete('/api/cadets/:id', async (req, res) => {
    try {
        const cadet = await Cadet.findByIdAndDelete(req.params.id);
        if (!cadet) return res.status(404).json({ message: 'Cadet not found' });
        res.status(204).json({ message: 'Cadet deleted successfully' });
    } catch (error) {
        res.status(500).json({ message: 'Error deleting cadet', error });
    }
});

// Blog Routes

// Create a New Blog Post
app.post('/api/blogs', async (req, res) => {
    try {
        const { title, content } = req.body;
        const newBlog = new Blog({ title, content });
        await newBlog.save();
        res.status(201).json({ message: 'Blog post created successfully', blog: newBlog });
    } catch (error) {
        res.status(500).json({ message: 'Error creating blog post', error });
    }
});

// Get All Blog Posts
app.get('/api/blogs', async (req, res) => {
    try {
        const blogs = await Blog.find();
        res.json(blogs);
    } catch (error) {
        res.status(500).json({ message: 'Error fetching blog posts', error });
    }
});

// Get a Blog Post by ID
app.get('/api/blogs/:id', async (req, res) => {
    try {
        const blog = await Blog.findById(req.params.id);
        if (!blog) return res.status(404).json({ message: 'Blog post not found' });
        res.json(blog);
    } catch (error) {
        res.status(500).json({ message: 'Error fetching blog post', error });
    }
});

// Update a Blog Post by ID
app.put('/api/blogs/:id', async (req, res) => {
    try {
        const { title, content } = req.body;
        const blog = await Blog.findByIdAndUpdate(req.params.id, { title, content }, { new: true });
        if (!blog) return res.status(404).json({ message: 'Blog post not found' });
        res.json(blog);
    } catch (error) {
        res.status(500).json({ message: 'Error updating blog post', error });
    }
});

// Delete a Blog Post by ID
app.delete('/api/blogs/:id', async (req, res) => {
    try {
        const blog = await Blog.findByIdAndDelete(req.params.id);
        if (!blog) return res.status(404).json({ message: 'Blog post not found' });
        res.status(204).json({ message: 'Blog post deleted successfully' });
    } catch (error) {
        res.status(500).json({ message: 'Error deleting blog post', error });
    }
});

// Start Server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
