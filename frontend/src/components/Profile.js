import React from "react";

function Profile({ user }) {
  return (
    <div className="profile-card">
      <h2>Profile</h2>
      <p><strong>ID:</strong> {user.id}</p>
      <p><strong>Full Name:</strong> {user.full_name || "N/A"}</p>
      <p><strong>Email:</strong> {user.email || "Hidden"}</p>
      <p><strong>Created At:</strong> {new Date(user.created_at).toLocaleString()}</p>
    </div>
  );
}

export default Profile;
