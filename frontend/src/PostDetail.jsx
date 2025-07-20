import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { useAuth } from "./AuthContext";
import './Home.css';

const API_URL = "http://127.0.0.1:8000/api/posts/";
const BACKEND_URL = "http://127.0.0.1:8000";

export default function PostDetail() {
  const { id } = useParams();
  const { user, token } = useAuth();
  const [post, setPost] = useState(null);
  const [comments, setComments] = useState([]);
  const [commentText, setCommentText] = useState("");
  const [error, setError] = useState("");
  const [likeCount, setLikeCount] = useState(0);
  const [dislikeCount, setDislikeCount] = useState(0);
  const [loading, setLoading] = useState(true);
  const [replyingTo, setReplyingTo] = useState(null);
  const [replyText, setReplyText] = useState("");
  const [loadingLike, setLoadingLike] = useState(false);

  const fetchPost = () => {
    fetch(`${API_URL}${id}/`)
      .then((res) => res.json())
      .then((data) => {
        setPost(data);
        setLikeCount(data.likes || 0);
        setDislikeCount(data.dislikes || 0);
      });
  };

  useEffect(() => {
    fetchPost();
    fetch(`${API_URL}${id}/comments/`)
      .then((res) => res.json())
      .then((data) => setComments(data.results || data))
      .catch(() => setError("Failed to load comments."))
      .finally(() => setLoading(false));
  }, [id]);

  const handleCommentSubmit = (e) => {
    e.preventDefault();
    if (!user) return;
    fetch(`${API_URL}${id}/comments/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ content: commentText }),
    })
      .then((res) => res.json())
      .then((data) => {
        setComments([data, ...comments]);
        setCommentText("");
        fetchPost(); // Re-fetch the post after adding a comment
      })
      .catch(() => setError("Failed to add comment."));
  };

  const handleReplySubmit = (commentId) => {
    fetch(`${BACKEND_URL}/api/comments/${commentId}/reply/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ content: replyText }),
    })
      .then(async (res) => {
        const data = await res.json();
        console.log('Reply response:', res.status, data);
        if (!res.ok) {
          if (data.error === 'This comment already has a reply.') {
            setReplyingTo(null);
            setReplyText("");
            setError('This comment already has a reply.');
            return;
          }
          throw new Error(data.error || 'Failed to reply');
        }
        setReplyingTo(null);
        setReplyText("");
        fetch(`${API_URL}${id}/comments/`)
          .then((res) => res.json())
          .then((data) => setComments(data.results || data));
      })
      .catch((err) => {
        setError(err.message);
        console.error('Reply error:', err);
      });
  };

  const handleLike = () => {
    setLoadingLike(true);
    fetch(`${API_URL}${id}/react/`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ action: "like" }),
    })
      .then(async res => {
        setLoadingLike(false);
        if (!res.ok) {
          setError("You must be logged in to like posts.");
          return;
        }
        const data = await res.json();
        setPost(data);
        setLikeCount(data.likes || 0);
        setDislikeCount(data.dislikes || 0);
      })
      .catch(() => {
        setLoadingLike(false);
        setError("Failed to like post.");
      });
  };

  const handleDislike = () => {
    setLoadingLike(true);
    fetch(`${API_URL}${id}/react/`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ action: "dislike" }),
    })
      .then(async res => {
        setLoadingLike(false);
        if (!res.ok) {
          setError("You must be logged in to dislike posts.");
          return;
        }
        const data = await res.json();
        setPost(data);
        setLikeCount(data.likes || 0);
        setDislikeCount(data.dislikes || 0);
      })
      .catch(() => {
        setLoadingLike(false);
        setError("Failed to dislike post.");
      });
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;
  if (!post) return <div>Post not found.</div>;

  const getImageUrl = (img) => {
    if (!img) return '';
    if (img.startsWith('http')) return img;
    return `http://127.0.0.1:8000${img}`;
  };

  return (
    <div className="post-detail">
      <h2>{post.title}</h2>
      {post.image && <img src={getImageUrl(post.image)} alt={post.title} className="post-detail-image" style={{ maxWidth: '100%', marginBottom: 16 }} />}
      <div className="post-detail-meta">
        <span>
          By {typeof post.author === 'object' && post.author !== null
            ? post.author.username
            : 'Unknown'}
        </span>
        <span>
          {" | "}
          {post.publish_date || post.created_at
            ? new Date(post.publish_date || post.created_at).toLocaleDateString()
            : ''}
        </span>
        <span>
          {" | Category: "}
          {typeof post.category === 'object' && post.category !== null
            ? post.category.name
            : 'Uncategorized'}
        </span>
      </div>
      <div className="post-detail-content">{post.content}</div>
      <div className="post-detail-tags">
        {post.tags && post.tags.map(tag => (
          <span key={tag.id || tag}>#{tag.name || tag} </span>
        ))}
      </div>
      <div className="post-detail-actions">
        <button onClick={handleLike} disabled={!user || loadingLike}>👍 {likeCount}</button>
        <button onClick={handleDislike} disabled={!user || loadingLike}>👎 {dislikeCount}</button>
      </div>
      <div className="post-detail-comments">
        <h3>Comments</h3>
        {comments.length === 0 && <div>No comments yet.</div>}
        {comments
          .filter(comment => !comment.parent) // Only top-level comments
          .map(comment => (
            <div key={comment.id} className="comment">
              <div className="comment-meta">
                <span>{comment.user || 'Unknown'}</span>
                <span> | {comment.created_at ? new Date(comment.created_at).toLocaleString() : ''}</span>
              </div>
              <div className="comment-text">{comment.content}</div>
              {user && (!comment.replies || comment.replies.length === 0) && (
                <button onClick={() => setReplyingTo(comment.id)} style={{ marginTop: '0.5rem' }}>
                  Reply
                </button>
              )}
              {replyingTo === comment.id && (
                <form onSubmit={e => { e.preventDefault(); handleReplySubmit(comment.id); }} className="comment-form" style={{ marginTop: '0.5rem' }}>
                  <textarea
                    value={replyText}
                    onChange={e => setReplyText(e.target.value)}
                    placeholder="Write your reply..."
                    required
                  />
                  <button type="submit">Submit Reply</button>
                  <button type="button" onClick={() => setReplyingTo(null)} style={{ marginLeft: '0.5rem' }}>Cancel</button>
                </form>
              )}
              {/* Show the first reply, if it exists */}
              {comment.replies && comment.replies.length > 0 && (
                <div className="comment reply" key={comment.replies[0].id} style={{ marginLeft: '2rem', background: '#23243a99' }}>
                  <div className="comment-meta">
                    <span>{comment.replies[0].user || 'Unknown'}</span>
                    <span> | {comment.replies[0].created_at ? new Date(comment.replies[0].created_at).toLocaleString() : ''}</span>
                  </div>
                  <div className="comment-text">{comment.replies[0].content}</div>
                </div>
              )}
            </div>
        ))}
        {user ? (
          <form onSubmit={handleCommentSubmit} className="comment-form">
            <textarea
              value={commentText}
              onChange={e => setCommentText(e.target.value)}
              placeholder="Add a comment..."
              required
            />
            <button type="submit">Submit</button>
          </form>
        ) : (
          <div>You must be logged in to comment.</div>
        )}
      </div>
    </div>
  );
} 