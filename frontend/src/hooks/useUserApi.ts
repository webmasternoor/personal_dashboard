// frontend/src/api/user/userService.ts

// Export the User interface so it can be imported by other components/hooks
export interface User {
    id: number;
    username: string;
    email: string;
    status: string; // e.g., 'Active', 'Inactive'
    created_at: string; // Assuming a date string
  }
  
  const API_BASE_URL = "http://127.0.0.1:5000";
  
  /**
   * Helper function to handle fetch responses and extract errors.
   * @param response The fetch Response object.
   * @returns A Promise that resolves with the JSON data or throws an error.
   */
  async function handleResponse<T>(response: Response): Promise<T> {
    if (!response.ok) {
      let errorMessage = "An unexpected error occurred";
      try {
        // Attempt to parse JSON error message from Flask
        const errorData = await response.json();
        errorMessage = errorData.error || errorData.message || JSON.stringify(errorData);
      } catch (e) {
        // If response is not JSON, use status text or a default
        errorMessage = response.statusText || "An unexpected error occurred";
      }
      throw new Error(errorMessage);
    }
    // If the response is successful but has no content (e.g., for DELETE/POST success with no body)
    // we might need to handle cases where response.json() would fail.
    // For now, assuming successful responses always have JSON content.
    return response.json();
  }
  
  /**
   * Fetches all users from the API.
   * @returns A Promise resolving to an array of User objects.
   */
  export const fetchUsersApi = async (): Promise<User[]> => {
    const response = await fetch(`${API_BASE_URL}/users`);
    return handleResponse<User[]>(response);
  };
  
  /**
   * Creates a new user via the API.
   * @param userData The data for the new user.
   * @returns A Promise that resolves when the user is created.
   */
  export const createUserApi = async (userData: { username: string; email: string; password?: string }): Promise<void> => {
    const response = await fetch(`${API_BASE_URL}/users`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(userData),
    });
    // We expect a 201 Created status, handleResponse will check for !ok
    await handleResponse<void>(response);
  };
  
  /**
   * Updates an existing user via the API.
   * @param userId The ID of the user to update.
   * @param userData The updated user data (username, email).
   * @returns A Promise that resolves when the user is updated.
   */
  export const updateUserApi = async (userId: number, userData: { username: string; email: string }): Promise<void> => {
    const response = await fetch(`${API_BASE_URL}/users/${userId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(userData),
    });
    await handleResponse<void>(response);
  };
  
  /**
   * Deletes a user via the API.
   * @param userId The ID of the user to delete.
   * @returns A Promise that resolves when the user is deleted.
   */
  export const deleteUserApi = async (userId: number): Promise<void> => {
    const response = await fetch(`${API_BASE_URL}/users/${userId}`, {
      method: "DELETE",
    });
    await handleResponse<void>(response);
  };
  
  // Add other API functions here if needed (e.g., login, logout, profile, settings)