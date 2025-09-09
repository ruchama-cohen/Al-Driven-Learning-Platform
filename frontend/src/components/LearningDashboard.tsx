import React, { useState, useEffect } from 'react';

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
  prompt: string;
  response: string;
  created_at: string;
}

interface LearningDashboardProps {
  userId: string;
}

const LearningDashboard: React.FC<LearningDashboardProps> = ({ userId }) => {
  const [categories, setCategories] = useState<Category[]>([]);
  const [subCategories, setSubCategories] = useState<SubCategory[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string>('');
  const [selectedSubCategory, setSelectedSubCategory] = useState<string>('');
  const [prompt, setPrompt] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState<string>('');
  const [history, setHistory] = useState<Prompt[]>([]);

  useEffect(() => {
    fetchCategories();
    fetchHistory();
  }, [userId]);

  useEffect(() => {
    if (selectedCategory) {
      fetchSubCategories(selectedCategory);
    }
  }, [selectedCategory]);

  const fetchCategories = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/categories');
      const data = await response.json();
      setCategories(Array.isArray(data) ? data : []);
    } catch (error) {
      console.error('Error fetching categories:', error);
      setCategories([]);
    }
  };

  const fetchSubCategories = async (categoryId: string) => {
    try {
      const response = await fetch(`http://localhost:8000/api/categories/${categoryId}/sub-categories`);
      const data = await response.json();
      setSubCategories(data);
    } catch (error) {
      console.error('Error fetching sub-categories:', error);
    }
  };

  const fetchHistory = async () => {
    try {
      const response = await fetch(`http://localhost:8000/api/users/${userId}/prompts`);
      const data = await response.json();
      setHistory(Array.isArray(data) ? data : []);
    } catch (error) {
      console.error('Error fetching history:', error);
      setHistory([]); 
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Form submitted!');
    console.log('Selected category:', selectedCategory);
    console.log('Selected sub-category:', selectedSubCategory);
    console.log('Prompt:', prompt);
    
    if (!selectedCategory || !prompt) {
      console.log('Missing required fields');
      alert('Please select a category and enter a question');
      return;
    }

    setLoading(true);
    try {
      console.log('Sending request to API...');
      const response = await fetch('http://localhost:8000/api/prompts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: userId,
          category_id: selectedCategory,
          sub_category_id: selectedSubCategory || 'general',
          prompt: prompt
        })
      });

      console.log('Response status:', response.status);
      
      if (response.ok) {
        const result = await response.json();
        console.log('API response:', result);
        setResponse(result.response);
        setPrompt('');
        fetchHistory();
      } else {
        console.error('API error:', response.status);
      }
    } catch (error) {
      console.error('Error submitting prompt:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="form-container">
        <h2>AI Learning Dashboard</h2>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Category:</label>
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
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

          {selectedCategory && (
            <div className="form-group">
              <label>Sub-Category:</label>
              <select
                value={selectedSubCategory}
                onChange={(e) => setSelectedSubCategory(e.target.value)}
                required
              >
                <option value="">Select a sub-category</option>
                {subCategories.map(subCategory => (
                  <option key={subCategory.id} value={subCategory.id}>
                    {subCategory.name}
                  </option>
                ))}
              </select>
            </div>
          )}

          <div className="form-group">
            <label>What would you like to learn?</label>
            <textarea
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="e.g., Teach me about black holes"
              rows={4}
              required
            />
          </div>

          <button type="submit" className="btn btn-primary" disabled={loading || !selectedCategory || !prompt}>
            {loading ? 'Generating Lesson...' : 'Get AI Lesson'}
          </button>
        </form>
      </div>

      {response && (
        <div className="form-container">
          <h3>AI Generated Lesson</h3>
          <div className="lesson-response">
            <pre>{response}</pre>
          </div>
        </div>
      )}

      <div className="list-container">
        <h3>Your Learning History</h3>
        {history.length === 0 ? (
          <p>No lessons yet. Start learning!</p>
        ) : (
          history.map(item => (
            <div key={item.id} className="list-item">
              <strong>Q: {item.prompt}</strong>
              <div className="lesson-preview">
                {item.response.substring(0, 200)}...
              </div>
              <small>{new Date(item.created_at).toLocaleDateString()}</small>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default LearningDashboard;