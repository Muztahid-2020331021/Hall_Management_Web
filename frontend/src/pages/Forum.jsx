// ================
// Forum.jsx
// ================

import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Forum = () => {
  const [posts, setPosts] = useState([]);
  const [textMessage, setTextMessage] = useState('');
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [fetching, setFetching] = useState(false);
  const [error, setError] = useState(null);

  const token = localStorage.getItem('access'); // Change if your token key is different

  const FILE_BASE_URL = 'http://localhost:8000/media/';

  // Fetch all forum posts
  const fetchPosts = async () => {
    setFetching(true);
    setError(null);
    try {
      const res = await axios.get('/forum/new_forum_post/', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setPosts(res.data.results || []);
    } catch (err) {
      console.error('Error fetching forum posts:', err);
      setError('Failed to load posts.');
    } finally {
      setFetching(false);
    }
  };

  useEffect(() => {
    fetchPosts();
  }, []);

  // Submit new forum post
  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!textMessage.trim() && files.length === 0) {
      alert('Please add text or file.');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      // 1. Create the post with text_message
      const res = await axios.post(
        '/forum/new_forum_post/',
        { text_message: textMessage.trim() },
        {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        }
      );

      const postId = res.data.post_id;

      // 2. Upload files one by one if any
      if (files.length > 0) {
        for (const file of files) {
          const formData = new FormData();
          formData.append('file', file);
          formData.append('post', postId);

          await axios.post('/forum/add_file/', formData, {
            headers: {
              Authorization: `Bearer ${token}`,
              'Content-Type': 'multipart/form-data',
            },
          });
        }
      }

      // Reset form inputs
      setTextMessage('');
      setFiles([]);

      // Refresh posts
      await fetchPosts();
    } catch (err) {
      console.error('Error creating forum post:', err);
      setError('Failed to post. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4 max-w-3xl mx-auto">
      <h2 className="text-xl font-bold mb-4">Forum</h2>

      <form onSubmit={handleSubmit} className="mb-6 space-y-4">
        <textarea
          className="w-full border p-2 rounded"
          rows={4}
          placeholder="Write something..."
          value={textMessage}
          onChange={(e) => setTextMessage(e.target.value)}
          disabled={loading}
        />

        <input
          type="file"
          multiple
          onChange={(e) => setFiles(Array.from(e.target.files))}
          disabled={loading}
        />

        <button
          type="submit"
          disabled={loading}
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 disabled:opacity-50"
        >
          {loading ? 'Posting...' : 'Post'}
        </button>
      </form>

      {fetching && <p>Loading posts...</p>}
      {error && <p className="text-red-600">{error}</p>}

      <div className="space-y-4">
        {posts.length === 0 && !fetching && <p>No posts yet.</p>}

        {posts.map((post) => (
          <div key={post.post_id} className="border p-4 rounded shadow">
            <div className="text-sm text-gray-600 mb-2">
              <strong>{post.user_email}</strong> —{' '}
              {post.post_date_time
                ? new Date(post.post_date_time).toLocaleString()
                : ''}
            </div>
            <p className="mb-2">{post.text_message}</p>

            {post.post_files &&
              Array.isArray(post.post_files) &&
              post.post_files.length > 0 && (
                <div className="space-y-1">
                  <strong>Attachments:</strong>
                  {post.post_files.map((file, idx) => (
                    <div key={idx}>
                      <a
                        href={`${FILE_BASE_URL}${file}`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-blue-600 underline"
                      >
                        {file.split('/').pop()}
                      </a>
                    </div>
                  ))}
                  
                </div>
              )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default Forum;
