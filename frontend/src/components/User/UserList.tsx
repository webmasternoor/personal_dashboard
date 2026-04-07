// frontend/src/components/User/UserList.tsx
import React, { useState } from 'react';
import './user.css'; // Import external CSS

// Import User interface from where it's defined (e.g., userService or a shared types file)
import { User } from '../../api/user/userService';

interface UserListProps {
  users: User[];
  onEdit: (user: User) => void;
  onDelete: (userId: number) => Promise<void>;
  loading: boolean; // Added loading state
  error: string | null; // Added error state
  // fetchUsers prop is removed if not used internally by UserList
}

const UserList: React.FC<UserListProps> = ({ users, onEdit, onDelete, loading, error }) => {
  const [searchTerm, setSearchTerm] = useState("");
  const [sortConfig, setSortConfig] = useState<{ key: keyof User; direction: 'ascending' | 'descending' } | null>(null);
  const [currentPage, setCurrentPage] = useState(1);
  const usersPerPage = 10;

  const handleSearchChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(event.target.value);
    setCurrentPage(1);
  };

  const requestSort = (key: keyof User) => {
    let direction: 'ascending' | 'descending' = 'ascending';
    if (sortConfig && sortConfig.key === key && sortConfig.direction === 'ascending') {
      direction = 'descending';
    }
    setSortConfig({ key, direction });
  };

  const getSortIndicator = (key: keyof User) => {
    if (!sortConfig || sortConfig.key !== key) return '';
    return sortConfig.direction === 'ascending' ? ' ▲' : ' ▼';
  };

  const filteredUsers = users.filter(user =>
    user.username.toLowerCase().includes(searchTerm.toLowerCase()) ||
    user.email.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const sortedUsers = [...filteredUsers].sort((a, b) => {
    if (!sortConfig) return 0;
    const aValue = a[sortConfig.key];
    const bValue = b[sortConfig.key];

    if (aValue < bValue) return sortConfig.direction === 'ascending' ? -1 : 1;
    if (aValue > bValue) return sortConfig.direction === 'ascending' ? 1 : -1;
    return 0;
  });

  const indexOfLastUser = currentPage * usersPerPage;
  const indexOfFirstUser = indexOfLastUser - usersPerPage;
  const currentUsers = sortedUsers.slice(indexOfFirstUser, indexOfLastUser);

  const paginate = (pageNumber: number) => setCurrentPage(pageNumber);
  const totalPages = Math.ceil(sortedUsers.length / usersPerPage);

  const handleClearFilters = () => {
    setSearchTerm("");
    setSortConfig(null);
    setCurrentPage(1);
  };

  // Conditional rendering for loading and error states
  if (loading) return <p className="message message-info">Loading users...</p>;
  if (error) return <p className="message message-error">Error: {error}</p>;
  if (users.length === 0 && !loading && !error) return <p className="message message-info">No users found.</p>;


  return (
    <div className="user-list-container">
      <h2>User List</h2>
      <div className="search-filter-bar">
        <input
          type="text"
          placeholder="Search by Name or Email..."
          value={searchTerm}
          onChange={handleSearchChange}
          className="search-input"
        />
        <button onClick={handleClearFilters} className="btn btn-clear-filters">
          Clear Filters
        </button>
      </div>

      <table className="user-table">
        <thead>
          <tr>
            <th onClick={() => requestSort('id')}>ID{getSortIndicator('id')}</th>
            <th onClick={() => requestSort('username')}>Name{getSortIndicator('username')}</th>
            <th>Email</th>
            <th onClick={() => requestSort('status')}>Status{getSortIndicator('status')}</th>
            <th onClick={() => requestSort('created_at')}>Created Date{getSortIndicator('created_at')}</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {currentUsers.length > 0 ? (
            currentUsers.map(user => (
              <tr key={user.id}>
                <td>{user.id}</td>
                <td>{user.username}</td>
                <td>{user.email}</td>
                <td>{user.status}</td>
                <td>{new Date(user.created_at).toLocaleDateString()}</td>
                <td className="actions">
                  <button onClick={() => onEdit(user)} className="btn-edit">Edit</button>
                  <button onClick={() => onDelete(user.id)} className="btn-delete">Delete</button>
                </td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan={6}>
                {searchTerm ? "No users found matching your search criteria." : "No users available."}
              </td>
            </tr>
          )}
        </tbody>
      </table>

      {totalPages > 1 && (
        <div className="pagination">
          <button onClick={() => paginate(currentPage - 1)} disabled={currentPage === 1}>Previous</button>
          {Array.from({ length: totalPages }, (_, i) => i + 1).map(pageNumber => (
            <button
              key={pageNumber}
              onClick={() => paginate(pageNumber)}
              className={currentPage === pageNumber ? "active-page" : ""}
            >
              {pageNumber}
            </button>
          ))}
          <button onClick={() => paginate(currentPage + 1)} disabled={currentPage === totalPages}>Next</button>
        </div>
      )}
    </div>
  );
}

export default UserList;