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
        <button
          onClick={handleLike}
          disabled={!user || loadingLike}
          style={{
            background: post && post.liked_by_me ? '#90ee90' : '',
            fontWeight: post && post.liked_by_me ? 'bold' : '',
            border: post && post.liked_by_me ? '2px solid #4caf50' : '',
            color: post && post.liked_by_me ? '#222' : '',
            transition: 'background 0.2s',
            marginRight: 8
          }}
          title={post && post.liked_by_me ? 'Remove like' : 'Like'}
        >
          👍 {likeCount}
        </button>
        <button
          onClick={handleDislike}
          disabled={!user || loadingLike}
          style={{
            background: post && post.disliked_by_me ? '#ffb6b6' : '',
            fontWeight: post && post.disliked_by_me ? 'bold' : '',
            border: post && post.disliked_by_me ? '2px solid #e53935' : '',
            color: post && post.disliked_by_me ? '#222' : '',
            transition: 'background 0.2s'
          }}
          title={post && post.disliked_by_me ? 'Remove dislike' : 'Dislike'}
        >
          👎 {dislikeCount}
        </button>
      </div>
      <div className="post-detail-comments mt-12">
        <h3 className="text-2xl font-bold mb-6 text-white drop-shadow-lg">Comments</h3>
        {comments.length === 0 && <div className="text-gray-300 italic mb-4">No comments yet.</div>}
        {comments
          .filter(comment => !comment.parent) // Only top-level comments
          .map(comment => (
            <div key={comment.id} className="comment mb-8 p-6 rounded-2xl bg-gradient-to-br from-indigo-900/70 via-purple-900/60 to-slate-900/80 shadow-xl border border-indigo-500/20">
              <div className="comment-label">Comment</div>
              <div className="comment-meta flex items-center gap-3 mb-2 text-sm text-indigo-200 font-semibold">
                <span className="inline-flex items-center gap-1"><span className="text-lg">👤</span>{comment.user || 'Unknown'}</span>
                <span className="text-xs text-indigo-300">| {comment.created_at ? new Date(comment.created_at).toLocaleString() : ''}</span>
              </div>
              <div className="comment-text text-lg text-white mb-2 break-words">{comment.content}</div>
              {user && (!comment.replies || comment.replies.length === 0) && (
                <button onClick={() => setReplyingTo(comment.id)} className="mt-2 px-4 py-1 rounded-lg bg-gradient-to-r from-indigo-500 to-pink-500 text-white font-semibold shadow hover:from-pink-500 hover:to-indigo-500 transition-colors">Reply</button>
              )}
              {replyingTo === comment.id && (
                <form onSubmit={e => { e.preventDefault(); handleReplySubmit(comment.id); }} className="comment-form mt-3 flex flex-col gap-2">
                  <textarea
                    value={replyText}
                    onChange={e => setReplyText(e.target.value)}
                    placeholder="Write your reply..."
                    required
                    className="rounded-xl bg-slate-800/80 border border-indigo-400/30 text-white p-3 focus:outline-none focus:ring-2 focus:ring-indigo-400 transition resize-none min-h-[60px]"
                  />
                  <div className="flex gap-2">
                    <button type="submit" className="px-4 py-1 rounded-lg bg-gradient-to-r from-indigo-500 to-pink-500 text-white font-semibold shadow hover:from-pink-500 hover:to-indigo-500 transition-colors">Submit Reply</button>
                    <button type="button" onClick={() => setReplyingTo(null)} className="px-4 py-1 rounded-lg bg-slate-700 text-gray-200 hover:bg-slate-600 transition">Cancel</button>
                  </div>
                </form>
              )}
              {/* Show the first reply, if it exists */}
              {comment.replies && comment.replies.length > 0 && (
                <div className="comment reply mt-4 ml-8 p-4 rounded-xl bg-gradient-to-br from-indigo-800/60 via-purple-800/50 to-slate-800/70 border border-indigo-400/10 shadow-inner">
                  <div className="reply-label">Reply</div>
                  <div className="comment-meta flex items-center gap-2 mb-1 text-xs text-pink-200 font-semibold">
                    <span className="inline-flex items-center gap-1"><span className="text-lg">👤</span>{comment.replies[0].user || 'Unknown'}</span>
                    <span className="text-xs text-pink-300">| {comment.replies[0].created_at ? new Date(comment.replies[0].created_at).toLocaleString() : ''}</span>
                  </div>
                  <div className="comment-text text-base text-pink-100 break-words">{comment.replies[0].content}</div>
                </div>
              )}
            </div>
        ))}
        {user ? (
          <form onSubmit={handleCommentSubmit} className="comment-form mt-10 flex flex-col gap-3 p-6 rounded-2xl bg-gradient-to-br from-indigo-900/60 via-purple-900/40 to-slate-900/60 shadow-lg border border-indigo-500/20">
            <textarea
              value={commentText}
              onChange={e => setCommentText(e.target.value)}
              placeholder="Add a comment..."
              required
              className="rounded-xl bg-slate-800/80 border border-indigo-400/30 text-white p-3 focus:outline-none focus:ring-2 focus:ring-indigo-400 transition resize-none min-h-[70px]"
            />
            <button type="submit" className="self-end px-6 py-2 rounded-lg bg-gradient-to-r from-indigo-500 to-pink-500 text-white font-bold shadow hover:from-pink-500 hover:to-indigo-500 transition-colors">Submit</button>
          </form>
        ) : (
          <div className="text-indigo-200 italic mt-6">You must be logged in to comment.</div>
        )}
      </div>
    </div>
  );
} 