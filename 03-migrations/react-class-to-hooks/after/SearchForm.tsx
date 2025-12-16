// @ts-nocheck
/**
 * SearchForm - Functional Component with Hooks (After Migration)
 * 
 * 📖 Book Reference: Chapter 7, Pattern 12 - Migration as Learning
 * 
 * Key transformations:
 * - Constructor state → useState
 * - createRef → useRef
 * - componentDidMount → useEffect
 * - Event handlers → useCallback (for those passed to children)
 * - setState with callback → functional form of setState
 * 
 * NOTE: This is demonstration code. Run `npm install` to enable type checking.
 */

import React, { useState, useRef, useEffect, useCallback } from 'react';

interface Props {
  onSearch: (query: string, filters: SearchFilters) => void;
  initialQuery?: string;
  placeholder?: string;
}

interface SearchFilters {
  category: string;
  sortBy: 'relevance' | 'date' | 'name';
  includeArchived: boolean;
}

const DEFAULT_FILTERS: SearchFilters = {
  category: 'all',
  sortBy: 'relevance',
  includeArchived: false,
};

/**
 * SearchForm Functional Component
 * 
 * Migration notes:
 * - Separate useState for query, filters, and isExpanded
 * - useRef replaces createRef
 * - useEffect for focus on mount
 * - Regular functions for simple handlers
 * - useCallback for handlers that update state with previous value
 */
function SearchForm({ onSearch, initialQuery = '', placeholder = 'Search...' }: Props) {
  // State - separate hooks for each piece of state
  const [query, setQuery] = useState(initialQuery);
  const [filters, setFilters] = useState<SearchFilters>({ ...DEFAULT_FILTERS });
  const [isExpanded, setIsExpanded] = useState(false);

  // Ref - useRef replaces createRef
  const inputRef = useRef<HTMLInputElement>(null);

  // Focus input on mount - replaces componentDidMount
  useEffect(() => {
    inputRef.current?.focus();
  }, []); // Empty deps = runs once on mount

  // Handle query input change
  const handleQueryChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    setQuery(e.target.value);
  }, []);

  // Handle category change - uses functional setState
  const handleCategoryChange = useCallback((e: React.ChangeEvent<HTMLSelectElement>) => {
    const newCategory = e.target.value;
    setFilters(prev => ({
      ...prev,
      category: newCategory,
    }));
  }, []);

  // Handle sort change - uses functional setState
  const handleSortChange = useCallback((e: React.ChangeEvent<HTMLSelectElement>) => {
    const newSort = e.target.value as SearchFilters['sortBy'];
    setFilters(prev => ({
      ...prev,
      sortBy: newSort,
    }));
  }, []);

  // Handle checkbox change - uses functional setState
  const handleArchivedChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const checked = e.target.checked;
    setFilters(prev => ({
      ...prev,
      includeArchived: checked,
    }));
  }, []);

  // Toggle expanded filters - uses functional setState
  const toggleExpanded = useCallback(() => {
    setIsExpanded(prev => !prev);
  }, []);

  // Reset filters to defaults
  const handleReset = useCallback(() => {
    setQuery('');
    setFilters({ ...DEFAULT_FILTERS });
    inputRef.current?.focus();
  }, []);

  // Handle form submission - uses onSearch from props
  const handleSubmit = useCallback((e: React.FormEvent) => {
    e.preventDefault();
    onSearch(query, filters);
  }, [onSearch, query, filters]);

  return (
    <form className="search-form" onSubmit={handleSubmit}>
      <div className="search-main">
        <input
          ref={inputRef}
          type="text"
          value={query}
          onChange={handleQueryChange}
          placeholder={placeholder}
          className="search-input"
        />
        <button type="submit" className="search-button">
          Search
        </button>
        <button
          type="button"
          onClick={toggleExpanded}
          className="filters-toggle"
        >
          {isExpanded ? 'Hide Filters' : 'Show Filters'}
        </button>
      </div>

      {isExpanded && (
        <div className="search-filters">
          <div className="filter-group">
            <label htmlFor="category">Category:</label>
            <select
              id="category"
              value={filters.category}
              onChange={handleCategoryChange}
            >
              <option value="all">All</option>
              <option value="documents">Documents</option>
              <option value="images">Images</option>
              <option value="videos">Videos</option>
            </select>
          </div>

          <div className="filter-group">
            <label htmlFor="sortBy">Sort By:</label>
            <select
              id="sortBy"
              value={filters.sortBy}
              onChange={handleSortChange}
            >
              <option value="relevance">Relevance</option>
              <option value="date">Date</option>
              <option value="name">Name</option>
            </select>
          </div>

          <div className="filter-group">
            <label>
              <input
                type="checkbox"
                checked={filters.includeArchived}
                onChange={handleArchivedChange}
              />
              Include Archived
            </label>
          </div>

          <button
            type="button"
            onClick={handleReset}
            className="reset-button"
          >
            Reset
          </button>
        </div>
      )}
    </form>
  );
}

export default SearchForm;
export type { SearchFilters };
