// frontend/src/components/User/UserManagement.tsx
import React, { useState, useEffect, useCallback } from 'react';
import UserForm from './UserForm';
import UserList from './UserList';
import './user.css'; // Import external CSS

// Import User interface from the API service file where it's defined and exported
import { User } from '../../api/user/userService';
import { fetchUsersApi, createUserApi, updateUserApi, deleteUserApi } from '../../api/user/userService';

const UserManagement: React.FC = () => {
  const [showForm, setShowForm] = useState(false);
  const [editingUser, setEditingUser] = useState<User | null>(null);
  const [users, setUsers] = useState<User[]>([]);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false); // Added loading state
  const [error, setError] = useState<string | null>(null); // Added error state

  const fetchUsers = useCallback(async (): Promise<User[]> => {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchUsersApi();
      setUsers(data);
      setMessage("Users loaded successfully");
      return data;
    } catch (err: any) {
      console.error("Error fetching users:", err);
      setError(`Failed to load users: ${err.message}`);
      setMessage(""); // Clear message on error
      return [];
    } finally {
      setLoading(false);
    }
  }, []);

  const createUser = async (userData: { username: string; email: string; password?: string }) => {
    setLoading(true);
    setError(null);
    try {
      await createUserApi(userData);
      await fetchUsers();
      setShowForm(false);
      setEditingUser(null);
      setMessage("User created successfully");
    } catch (error: any) {
      console.error("Error creating user:", error);
      setError(`Failed to create user: ${error.message}`);
      setMessage(""); // Clear message on error
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const updateUser = async (userId: number, userData: { username: string; email: string }) => {
    setLoading(true);
    setError(null);
    try {
      await updateUserApi(userId, userData);
      await fetchUsers();
      setShowForm(false);
      setEditingUser(null);
      setMessage("User updated successfully");
    } catch (error: any) {
      console.error("Error updating user:", error);
      setError(`Failed to update user: ${error.message}`);
      setMessage(""); // Clear message on error
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const deleteUser = async (userId: number) => {
    setLoading(true);
    setError(null);
    if (window.confirm("Are you sure you want to delete this user?")) {
      try {
        await deleteUserApi(userId);
        await fetchUsers();
        setMessage("User deleted successfully");
      } catch (error: any) {
        console.error("Error deleting user:", error);
        setError(`Failed to delete user: ${error.message}`);
        setMessage(""); // Clear message on error
      } finally {
        setLoading(false);
      }
    } else {
      setLoading(false); // If cancelled, stop loading state
    }
  };

  const handleEdit = (user: User) => {
    setEditingUser(user);
    setShowForm(true);
  };

  const handleCancelForm = () => {
    setShowForm(false);
    setEditingUser(null);
  };

  const handleFormSubmit = async (userData: { username: string; email: string; password?: string }) => {
    if (editingUser) {
      await updateUser(editingUser.id, { username: userData.username, email: userData.email });
    } else {
      await createUser(userData);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, [fetchUsers]);



  const handleAddUserClick = () => {
    setEditingUser(null);
    setShowForm(true);
  };


  return (
    <div className="user-management-container">
      <h1>User Management</h1>

      {!showForm && (
        <button onClick={handleAddUserClick} className="btn btn-primary btn-add-user"> Add New User </button>
      )}

      {showForm && (
        <UserForm
          formTitle={editingUser ? "Edit User" : "Create New User"}
          submitButtonText={editingUser ? "Update User" : "Create User"}
          initialValues={editingUser ? { username: editingUser.username, email: editingUser.email } : undefined}
          onSubmit={handleFormSubmit}
          onCancel={handleCancelForm}
        />
      )}

      <UserList
        users={users}
        onEdit={handleEdit}
        onDelete={deleteUser}
        loading={loading}
        error={error}
      />
      {message && <p className={`message ${message.startsWith("✅") ? "message-success" : "message-error"}`}>{message}</p>}
    </div>
  );
}

export default UserManagement;