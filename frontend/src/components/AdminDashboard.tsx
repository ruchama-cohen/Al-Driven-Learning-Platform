import React, { useState, useEffect } from 'react';

interface User {
  id: string;
  name: string;
  phone: string;
}

interface Prompt {
  id: string;
  user_id: string;
  prompt: string;
  response: string;
  created_at: string;
}

interface Category {
  id: string;
  name: string;
}

const AdminDashboard: React.FC = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [prompts, setPrompts] = useState<Prompt[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [newCategory, setNewCategory] = useState('');
  const [newSubCategory, setNewSubCategory] = useState('');
  const [selectedCategoryForSub, setSelectedCategoryForSub] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>('');
  const [subCategories, setSubCategories] = useState<any[]>([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    fetchUsers(currentPage, searchTerm);
    fetchPrompts();
    fetchCategories();
    fetchSubCategories();
  }, [currentPage, searchTerm]);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    setCurrentPage(1);
    fetchUsers(1, searchTerm);
  };

  const fetchUsers = async (page = 1, search = '') => {
    try {
      const url = `http://localhost:8000/api/users?page=${page}&limit=10${search ? `&search=${search}` : ''}`;
      const response = await fetch(url);
      const data = await response.json();
      if (data.users) {
        setUsers(data.users);
        setTotalPages(data.pages);
        setCurrentPage(page);
      } else {
        setUsers([]);
      }
    } catch (error) {
      console.error('Error fetching users:', error);
      setUsers([]);
    }
  };

  const fetchPrompts = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/prompts');
      const data = await response.json();
      setPrompts(Array.isArray(data) ? data : []);
    } catch (error) {
      console.error('Error fetching prompts:', error);
      setPrompts([]);
    }
  };

  const fetchCategories = async () => {
    try {
      setError('');
      const response = await fetch('http://localhost:8000/api/categories');
      const data = await response.json();
      console.log('Categories data from server:', data);
      
      if (!Array.isArray(data)) {
        console.error('Server returned non-array data:', data);
        setError('Invalid data format received from server');
        setCategories([]);
        return;
      }
      
      setCategories(data);
    } catch (error) {
      console.error('Error fetching categories:', error);
      setError('Failed to fetch categories. Please try again later.');
      setCategories([]);
    }
  };

  const fetchSubCategories = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/sub-categories');
      const data = await response.json();
      setSubCategories(Array.isArray(data) ? data : []);
    } catch (error) {
      console.error('Error fetching sub-categories:', error);
      setSubCategories([]);
    }
  };

  const handleAddCategory = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newCategory) return;

    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/categories', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: newCategory })
      });

      if (response.ok) {
        setNewCategory('');
        fetchCategories();
      }
    } catch (error) {
      console.error('Error adding category:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAddSubCategory = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newSubCategory || !selectedCategoryForSub) return;

    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/sub-categories', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          name: newSubCategory,
          category_id: selectedCategoryForSub
        })
      });

      if (response.ok) {
        setNewSubCategory('');
        setSelectedCategoryForSub('');
        fetchSubCategories();
      }
    } catch (error) {
      console.error('Error adding sub-category:', error);
    } finally {
      setLoading(false);
    }
  };

  const getUserName = (userId: string) => {
    const user = users.find(u => u.id === userId);
    return user ? user.name : 'Unknown User';
  };

  return (
    <div>
      <div className="form-container">
        <h2>Admin Dashboard</h2>
        
        {error && (
          <div style={{ color: 'red', padding: '10px', marginBottom: '10px' }}>
            {error}
          </div>
        )}
        
        <div className="admin-section">
          <h3>Add New Category</h3>
          <form onSubmit={handleAddCategory}>
            <div className="form-group">
              <input
                type="text"
                value={newCategory}
                onChange={(e) => setNewCategory(e.target.value)}
                placeholder="Category name (e.g., Science, History)"
                required
              />
              <button type="submit" className="btn btn-primary" disabled={loading}>
                {loading ? 'Adding...' : 'Add Category'}
              </button>
            </div>
          </form>
        </div>

        <div className="admin-section">
          <h3>Add New Sub-Category</h3>
          <form onSubmit={handleAddSubCategory}>
            <div className="form-group">
              <select
                value={selectedCategoryForSub}
                onChange={(e) => setSelectedCategoryForSub(e.target.value)}
                required
              >
                <option value="">Select a category</option>
                {categories.map(category => (
                  <option key={category.id} value={category.id}>
                    {category.name}
                  </option>
                ))}
              </select>
            </div>
            <div className="form-group">
              <input
                type="text"
                value={newSubCategory}
                onChange={(e) => setNewSubCategory(e.target.value)}
                placeholder="Sub-category name (e.g., Physics, Chemistry)"
                required
              />
              <button type="submit" className="btn btn-primary" disabled={loading || !selectedCategoryForSub}>
                {loading ? 'Adding...' : 'Add Sub-Category'}
              </button>
            </div>
          </form>
        </div>
      </div>

      <div className="list-container">
        <h3>All Users</h3>
        
        {/* Search */}
        <form onSubmit={handleSearch} style={{ marginBottom: '20px' }}>
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Search users by name or phone..."
            style={{ marginRight: '10px', padding: '5px' }}
          />
          <button type="submit" className="btn btn-primary">Search</button>
        </form>
        
        {/* Users List */}
        {users.map(user => (
          <div key={user.id} className="list-item">
            <strong>{user.name}</strong> - {user.phone}
            <small> (ID: {user.id})</small>
          </div>
        ))}
        
        {/* Pagination */}
        <div style={{ marginTop: '20px', textAlign: 'center' }}>
          <button 
            onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
            disabled={currentPage === 1}
            className="btn btn-primary"
            style={{ marginRight: '10px' }}
          >
            Previous
          </button>
          
          <span>Page {currentPage} of {totalPages}</span>
          
          <button 
            onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages))}
            disabled={currentPage === totalPages}
            className="btn btn-primary"
            style={{ marginLeft: '10px' }}
          >
            Next
          </button>
        </div>
      </div>

      <div className="list-container">
        <h3>Categories ({categories.length})</h3>
        {categories.map(category => (
          <div key={category.id} className="list-item">
            <strong>{category.name}</strong>
            <small> (ID: {category.id})</small>
          </div>
        ))}
      </div>

      <div className="list-container">
        <h3>Sub-Categories ({subCategories.length})</h3>
        {subCategories.map(subCategory => (
          <div key={subCategory.id} className="list-item">
            <strong>{subCategory.name}</strong>
            <small> (Category: {categories.find(c => c.id === subCategory.category_id)?.name || 'Unknown'})</small>
          </div>
        ))}
      </div>

      <div className="list-container">
        <h3>All Learning Activity ({prompts.length} lessons)</h3>
        {prompts.length === 0 ? (
          <p>No learning activity yet.</p>
        ) : (
          prompts.map(prompt => (
            <div key={prompt.id} className="list-item">
              <div>
                <strong>User:</strong> {getUserName(prompt.user_id)}
              </div>
              <div>
                <strong>Question:</strong> {prompt.prompt}
              </div>
              <div className="lesson-preview">
                <strong>Response:</strong> {prompt.response.substring(0, 150)}...
              </div>
              <small>{new Date(prompt.created_at).toLocaleDateString()}</small>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default AdminDashboard;