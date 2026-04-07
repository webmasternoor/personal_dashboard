// frontend/src/components/User/UserForm.tsx
import React, { useState, useEffect } from 'react';
import './user.css'; // Import external CSS

// Define UserFormProps here or import from a shared types file
interface UserFormProps {
  initialValues?: { username: string; email: string; password?: string };
  onSubmit: (userData: { username: string; email: string; password?: string }) => Promise<void>;
  formTitle: string;
  submitButtonText: string;
  onCancel?: () => void;
}

const UserForm: React.FC<UserFormProps> = ({
  initialValues,
  onSubmit,
  formTitle,
  submitButtonText,
  onCancel,
}) => {
  const [username, setUsername] = useState(initialValues?.username || "");
  const [email, setEmail] = useState(initialValues?.email || "");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  useEffect(() => {
    setUsername(initialValues?.username || "");
    setEmail(initialValues?.email || "");
    if (!initialValues) {
      setPassword("");
    }
  }, [initialValues]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setMessage("");

    try {
      const userData = submitButtonText === "Create User"
        ? { username, email, password }
        : { username, email };

      await onSubmit(userData);

      if (submitButtonText === "Create User") {
        setUsername("");
        setEmail("");
        setPassword("");
      }
      setMessage("Operation successful!");
    } catch (error: any) {
      console.error("Form submission error:", error);
      setMessage(`❌ ${error.message || "Operation failed"}`);
    }
  };

  return (
    <div className="user-form-container">
      <h2>{formTitle}</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        {submitButtonText === "Create User" && (
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        )}
        <button type="submit" className="btn btn-submit">
          {submitButtonText}
        </button>
        {onCancel && (
          <button type="button" onClick={onCancel} className="btn btn-cancel">
            Cancel
          </button>
        )}
      </form>

      {message && <p className={`message ${message.startsWith("✅") ? "message-success" : "message-error"}`}>{message}</p>}
    </div>
  );
}

export default UserForm;