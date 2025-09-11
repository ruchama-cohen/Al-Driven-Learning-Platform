import React, { useState, useEffect } from 'react';
import './AdminDashboard.css';

interface User {
  id: string;
  name: string;
  phone: string;
  id_number: string;
  created_at: string;
}

interface Category {
  id: string;
  name: string;
}

interface SubCategory {
  id: string;
  name: string;
  category_id: string;
}

interface Prompt {
  id: string;
  user_id: string;
  prompt: string;
  response: string;
  created_at: string;
}

interface PaginatedUsers {
  users: User[];
  total: number;
  page: number;
  limit: number;
  pages: number;
  has_next: boolean;
  has_prev: boolean;
}

const AdminDashboard: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'users' | 'categories' | 'prompts' | 'stats'>('users');
  
  const [users, setUsers] = useState<PaginatedUsers>({
    users: [],
    total: 0,
    page: 1,
    limit: 10,
    pages: 0,
    has_next: false,
    has_prev: false
  });
  const [usersLoading, setUsersLoading] = useState(false);
  const [usersSearch, setUsersSearch] = useState('');
  const [usersSortBy, setUsersSortBy] = useState('created_at');
  const [usersSortOrder, setUsersSortOrder] = useState('desc');
  
  const [categories, setCategories] = useState<Category[]>([]);
  const [subCategories, setSubCategories] = useState<SubCategory[]>([]);
  const [newCategoryName, setNewCategoryName] = useState('');
  const [newSubCategoryName, setNewSubCategoryName] = useState('');
  const [selectedCategoryForSub, setSelectedCategoryForSub] = useState('');
  
  const [prompts, setPrompts] = useState<Prompt[]>([]);
  const [promptsLoading, setPromptsLoading] = useState(false);
  
  const [stats, setStats] = useState({
    totalUsers: 0,
    totalCategories: 0,
    totalPrompts: 0,
    recentActivity: []
  });

  useEffect(() => {
    fetchUsers();
    fetchCategories();
    fetchSubCategories();
    fetchPrompts();
    fetchStats();
  }, []);

  const fetchUsers = async (page = 1, search = '', sortBy = 'created_at', sortOrder = 'desc') => {
    setUsersLoading(true);
    try {
      const params = new URLSearchParams({
        page: page.toString(),
        limit: '10',
        ...(search && { search }),
        sort_by: sortBy,
        sort_order: sortOrder
      });

      const response = await fetch(`http://localhost:8000/api/users?${params}`);
      const data = await response.json();
      setUsers(data);
    } catch (error) {
      console.error('Error fetching users:', error);
    } finally {
      setUsersLoading(false);
    }
  };

  const handleUsersSearch = (e: React.FormEvent) => {
    e.preventDefault();
    fetchUsers(1, usersSearch, usersSortBy, usersSortOrder);
  };

  const handleUsersSortChange = (field: string) => {
    const newOrder = field === usersSortBy && usersSortOrder === 'asc' ? 'desc' : 'asc';
    setUsersSortBy(field);
    setUsersSortOrder(newOrder);
    fetchUsers(users.page, usersSearch, field, newOrder);
  };

  const deleteUser = async (userId: string) => {
    if (!window.confirm('Are you sure you want to delete this user?')) return;
    
    try {
      const response = await fetch(`http://localhost:8000/api/users/${userId}`, {
        method: 'DELETE'
      });
      
      if (response.ok) {
        fetchUsers(users.page, usersSearch, usersSortBy, usersSortOrder);
        alert('User deleted successfully');
      }
    } catch (error) {
      console.error('Error deleting user:', error);
      alert('Error deleting user');
    }
  };

  const fetchCategories = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/categories');
      const data = await response.json();
      setCategories(Array.isArray(data) ? data : []);
    } catch (error) {
      console.error('Error fetching categories:', error);
    }
  };

  const fetchSubCategories = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/sub-categories');
      const data = await response.json();
      setSubCategories(Array.isArray(data) ? data : []);
    } catch (error) {
      console.error('Error fetching sub-categories:', error);
    }
  };

  const createCategory = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newCategoryName.trim()) return;

    try {
      const response = await fetch('http://localhost:8000/api/categories', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: newCategoryName })
      });

      if (response.ok) {
        setNewCategoryName('');
        fetchCategories();
        alert('Category created successfully');
      }
    } catch (error) {
      console.error('Error creating category:', error);
    }
  };

  const createSubCategory = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newSubCategoryName.trim() || !selectedCategoryForSub) return;

    try {
      const response = await fetch('http://localhost:8000/api/sub-categories', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: newSubCategoryName,
          category_id: selectedCategoryForSub
        })
      });

      if (response.ok) {
        setNewSubCategoryName('');
        setSelectedCategoryForSub('');
        fetchSubCategories();
        alert('Sub-category created successfully');
      }
    } catch (error) {
      console.error('Error creating sub-category:', error);
    }
  };

  const deleteSubCategory = async (subCategoryId: string) => {
    if (!window.confirm('Are you sure you want to delete this sub-category?')) return;
    
    try {
      const response = await fetch(`http://localhost:8000/api/sub-categories/${subCategoryId}`, {
        method: 'DELETE'
      });
      
      if (response.ok) {
        fetchSubCategories();
        alert('Sub-category deleted successfully');
      }
    } catch (error) {
      console.error('Error deleting sub-category:', error);
    }
  };

  const fetchPrompts = async () => {
    setPromptsLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/prompts');
      const data = await response.json();
      setPrompts(Array.isArray(data) ? data : []);
    } catch (error) {
      console.error('Error fetching prompts:', error);
    } finally {
      setPromptsLoading(false);
    }
  };

  const fetchStats = async () => {
    try {
      setStats({
        totalUsers: users.total || 0,
        totalCategories: categories.length,
        totalPrompts: prompts.length,
        recentActivity: []
      });
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  return (
    <div className="admin-dashboard">
      <div className="admin-header">
        <h1>Admin Dashboard</h1>
        <div className="admin-tabs">
          <button
            className={activeTab === 'users' ? 'active' : ''}
            onClick={() => setActiveTab('users')}
          >
            Users ({users.total})
          </button>
          <button
            className={activeTab === 'categories' ? 'active' : ''}
            onClick={() => setActiveTab('categories')}
          >
            Categories ({categories.length})
          </button>
          <button
            className={activeTab === 'prompts' ? 'active' : ''}
            onClick={() => setActiveTab('prompts')}
          >
            Lessons ({prompts.length})
          </button>
          <button
            className={activeTab === 'stats' ? 'active' : ''}
            onClick={() => setActiveTab('stats')}
          >
            Statistics
          </button>
        </div>
      </div>

      <div className="admin-content">
        {activeTab === 'users' && (
          <div className="users-tab">
            <div className="users-controls">
              <form onSubmit={handleUsersSearch} className="search-form">
                <input
                  type="text"
                  placeholder="Search users..."
                  value={usersSearch}
                  onChange={(e) => setUsersSearch(e.target.value)}
                />
                <button type="submit">Search</button>
                <button type="button" onClick={() => {
                  setUsersSearch('');
                  fetchUsers(1);
                }}>
                  Clear
                </button>
              </form>
              
              <div className="sort-controls">
                <label>Sort by:</label>
                <select 
                  value={usersSortBy} 
                  onChange={(e) => handleUsersSortChange(e.target.value)}
                >
                  <option value="created_at">Date Created</option>
                  <option value="name">Name</option>
                  <option value="phone">Phone</option>
                </select>
                <button onClick={() => handleUsersSortChange(usersSortBy)}>
                  {usersSortOrder === 'asc' ? '↑' : '↓'}
                </button>
              </div>
            </div>

            <div className="users-table">
              {usersLoading ? (
                <div className="loading">Loading users...</div>
              ) : (
                <>
                  <table>
                    <thead>
                      <tr>
                        <th onClick={() => handleUsersSortChange('name')}>
                          Name {usersSortBy === 'name' && (usersSortOrder === 'asc' ? '↑' : '↓')}
                        </th>
                        <th onClick={() => handleUsersSortChange('phone')}>
                          Phone {usersSortBy === 'phone' && (usersSortOrder === 'asc' ? '↑' : '↓')}
                        </th>
                        <th>ID Number</th>
                        <th onClick={() => handleUsersSortChange('created_at')}>
                          Created {usersSortBy === 'created_at' && (usersSortOrder === 'asc' ? '↑' : '↓')}
                        </th>
                        <th>Actions</th>
                      </tr>
                    </thead>
                    <tbody>
                      {users.users.map(user => (
                        <tr key={user.id}>
                          <td>{user.name}</td>
                          <td>{user.phone}</td>
                          <td>{user.id_number}</td>
                          <td>{new Date(user.created_at).toLocaleDateString()}</td>
                          <td>
                            <button 
                              className="btn-danger"
                              onClick={() => deleteUser(user.id)}
                            >
                              Delete
                            </button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>

                  <div className="pagination">
                    <button
                      disabled={!users.has_prev}
                      onClick={() => fetchUsers(users.page - 1, usersSearch, usersSortBy, usersSortOrder)}
                    >
                      Previous
                    </button>
                    
                    <span>
                      Page {users.page} of {users.pages} ({users.total} total users)
                    </span>
                    
                    <button
                      disabled={!users.has_next}
                      onClick={() => fetchUsers(users.page + 1, usersSearch, usersSortBy, usersSortOrder)}
                    >
                      Next
                    </button>
                  </div>
                </>
              )}
            </div>
          </div>
        )}

        {activeTab === 'categories' && (
          <div className="categories-tab">
            <div className="categories-section">
              <h3>Create New Category</h3>
              <form onSubmit={createCategory} className="create-form">
                <input
                  type="text"
                  placeholder="Category name"
                  value={newCategoryName}
                  onChange={(e) => setNewCategoryName(e.target.value)}
                  required
                />
                <button type="submit">Create Category</button>
              </form>

              <h3>Existing Categories</h3>
              <div className="categories-list">
                {categories.map(category => (
                  <div key={category.id} className="category-item">
                    <strong>{category.name}</strong>
                    <span>({subCategories.filter(sub => sub.category_id === category.id).length} sub-categories)</span>
                  </div>
                ))}
              </div>
            </div>

            <div className="subcategories-section">
              <h3>Create New Sub-Category</h3>
              <form onSubmit={createSubCategory} className="create-form">
                <select
                  value={selectedCategoryForSub}
                  onChange={(e) => setSelectedCategoryForSub(e.target.value)}
                  required
                >
                  <option value="">Select Category</option>
                  {categories.map(category => (
                    <option key={category.id} value={category.id}>
                      {category.name}
                    </option>
                  ))}
                </select>
                <input
                  type="text"
                  placeholder="Sub-category name"
                  value={newSubCategoryName}
                  onChange={(e) => setNewSubCategoryName(e.target.value)}
                  required
                />
                <button type="submit">Create Sub-Category</button>
              </form>

              <h3>Existing Sub-Categories</h3>
              <div className="subcategories-list">
                {subCategories.map(subCategory => {
                  const category = categories.find(c => c.id === subCategory.category_id);
                  return (
                    <div key={subCategory.id} className="subcategory-item">
                      <strong>{subCategory.name}</strong>
                      <span>in {category?.name || 'Unknown Category'}</span>
                      <button 
                        className="btn-danger"
                        onClick={() => deleteSubCategory(subCategory.id)}
                      >
                        Delete
                      </button>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'prompts' && (
          <div className="prompts-tab">
            <h3>All AI Lessons</h3>
            {promptsLoading ? (
              <div className="loading">Loading lessons...</div>
            ) : (
              <div className="prompts-list">
                {prompts.map(prompt => (
                  <div key={prompt.id} className="prompt-item">
                    <div className="prompt-header">
                      <strong>Q: {prompt.prompt}</strong>
                      <small>{new Date(prompt.created_at).toLocaleDateString()}</small>
                    </div>
                    <div className="prompt-preview">
                      {prompt.response.substring(0, 200)}...
                    </div>
                    <div className="prompt-meta">
                      <span>User ID: {prompt.user_id}</span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {activeTab === 'stats' && (
          <div className="stats-tab">
            <h3>Platform Statistics</h3>
            <div className="stats-grid">
              <div className="stat-card">
                <h4>Total Users</h4>
                <p className="stat-number">{users.total}</p>
              </div>
              <div className="stat-card">
                <h4>Total Categories</h4>
                <p className="stat-number">{categories.length}</p>
              </div>
              <div className="stat-card">
                <h4>Total Sub-Categories</h4>
                <p className="stat-number">{subCategories.length}</p>
              </div>
              <div className="stat-card">
                <h4>Total Lessons</h4>
                <p className="stat-number">{prompts.length}</p>
              </div>
            </div>
            
            <div className="recent-activity">
              <h4>Recent Activity</h4>
              <p>Recent activity tracking will be implemented here</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AdminDashboard;