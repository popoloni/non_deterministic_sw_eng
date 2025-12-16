/**
 * SearchForm - Class Component (Before Migration)
 * 
 * 📖 Book Reference: Chapter 7, Pattern 12 - Migration as Learning
 * 
 * This demonstrates controlled form inputs and event handling in class components.
 */

import React from 'react';

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

interface State {
  query: string;
  filters: SearchFilters;
  isExpanded: boolean;
}

const DEFAULT_FILTERS: SearchFilters = {
  category: 'all',
  sortBy: 'relevance',
  includeArchived: false,
};

/**
 * SearchForm Class Component
 * 
 * Patterns used:
 * - Controlled inputs with state
 * - Event handlers for form elements
 * - Derived state from props
 * - Complex state object
 */
class SearchForm extends React.Component<Props, State> {
  // Input ref for focusing
  private inputRef = React.createRef<HTMLInputElement>();

  constructor(props: Props) {
    super(props);
    
    this.state = {
      query: props.initialQuery || '',
      filters: { ...DEFAULT_FILTERS },
      isExpanded: false,
    };
  }

  // Focus input on mount
  componentDidMount() {
    this.inputRef.current?.focus();
  }

  // Handle query input change
  handleQueryChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    this.setState({ query: e.target.value });
  };

  // Handle category change
  handleCategoryChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    this.setState(prevState => ({
      filters: {
        ...prevState.filters,
        category: e.target.value,
      },
    }));
  };

  // Handle sort change
  handleSortChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    this.setState(prevState => ({
      filters: {
        ...prevState.filters,
        sortBy: e.target.value as SearchFilters['sortBy'],
      },
    }));
  };

  // Handle checkbox change
  handleArchivedChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    this.setState(prevState => ({
      filters: {
        ...prevState.filters,
        includeArchived: e.target.checked,
      },
    }));
  };

  // Toggle expanded filters
  toggleExpanded = () => {
    this.setState(prevState => ({
      isExpanded: !prevState.isExpanded,
    }));
  };

  // Reset filters to defaults
  handleReset = () => {
    this.setState({
      query: '',
      filters: { ...DEFAULT_FILTERS },
    });
    this.inputRef.current?.focus();
  };

  // Handle form submission
  handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const { query, filters } = this.state;
    this.props.onSearch(query, filters);
  };

  render() {
    const { placeholder = 'Search...' } = this.props;
    const { query, filters, isExpanded } = this.state;

    return (
      <form className="search-form" onSubmit={this.handleSubmit}>
        <div className="search-main">
          <input
            ref={this.inputRef}
            type="text"
            value={query}
            onChange={this.handleQueryChange}
            placeholder={placeholder}
            className="search-input"
          />
          <button type="submit" className="search-button">
            Search
          </button>
          <button
            type="button"
            onClick={this.toggleExpanded}
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
                onChange={this.handleCategoryChange}
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
                onChange={this.handleSortChange}
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
                  onChange={this.handleArchivedChange}
                />
                Include Archived
              </label>
            </div>

            <button
              type="button"
              onClick={this.handleReset}
              className="reset-button"
            >
              Reset
            </button>
          </div>
        )}
      </form>
    );
  }
}

export default SearchForm;
export type { SearchFilters };
