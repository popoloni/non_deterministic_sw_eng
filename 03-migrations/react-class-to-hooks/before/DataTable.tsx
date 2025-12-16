/**
 * DataTable - Class Component (Before Migration)
 * 
 * 📖 Book Reference: Chapter 7, Pattern 12 - Migration as Learning
 * 
 * This is a complex component demonstrating:
 * - Multiple state variables
 * - Multiple lifecycle methods
 * - Complex event handling
 * - Performance optimization with shouldComponentUpdate
 */

import React from 'react';

// Types
interface Column<T> {
  key: keyof T;
  label: string;
  sortable?: boolean;
  render?: (value: T[keyof T], row: T) => React.ReactNode;
}

interface Props<T> {
  data: T[];
  columns: Column<T>[];
  pageSize?: number;
  onRowClick?: (row: T) => void;
  onSelectionChange?: (selected: T[]) => void;
}

interface State<T> {
  currentPage: number;
  sortColumn: keyof T | null;
  sortDirection: 'asc' | 'desc';
  selectedRows: Set<number>;
  searchTerm: string;
}

/**
 * DataTable Class Component
 * 
 * This component demonstrates complex state management and
 * lifecycle methods that need careful migration to hooks.
 */
class DataTable<T extends { id: string | number }> extends React.Component<
  Props<T>,
  State<T>
> {
  // Debounce timer for search
  private searchTimer: ReturnType<typeof setTimeout> | null = null;

  constructor(props: Props<T>) {
    super(props);

    this.state = {
      currentPage: 1,
      sortColumn: null,
      sortDirection: 'asc',
      selectedRows: new Set(),
      searchTerm: '',
    };
  }

  // Reset pagination when data changes
  componentDidUpdate(prevProps: Props<T>) {
    if (prevProps.data !== this.props.data) {
      this.setState({ currentPage: 1, selectedRows: new Set() });
    }
  }

  // Cleanup timer on unmount
  componentWillUnmount() {
    if (this.searchTimer) {
      clearTimeout(this.searchTimer);
    }
  }

  // Performance optimization
  shouldComponentUpdate(nextProps: Props<T>, nextState: State<T>) {
    // Skip update if only searchTerm changed (debounced)
    if (
      this.state.searchTerm !== nextState.searchTerm &&
      this.state.currentPage === nextState.currentPage &&
      this.state.sortColumn === nextState.sortColumn &&
      this.state.sortDirection === nextState.sortDirection &&
      this.state.selectedRows === nextState.selectedRows &&
      this.props.data === nextProps.data
    ) {
      return false;
    }
    return true;
  }

  // Get processed data (sorted and filtered)
  getProcessedData(): T[] {
    const { data } = this.props;
    const { sortColumn, sortDirection, searchTerm } = this.state;

    let processed = [...data];

    // Filter by search term
    if (searchTerm) {
      const term = searchTerm.toLowerCase();
      processed = processed.filter(row =>
        Object.values(row).some(value =>
          String(value).toLowerCase().includes(term)
        )
      );
    }

    // Sort
    if (sortColumn) {
      processed.sort((a, b) => {
        const aVal = a[sortColumn];
        const bVal = b[sortColumn];

        if (aVal < bVal) return sortDirection === 'asc' ? -1 : 1;
        if (aVal > bVal) return sortDirection === 'asc' ? 1 : -1;
        return 0;
      });
    }

    return processed;
  }

  // Get current page data
  getCurrentPageData(): T[] {
    const { pageSize = 10 } = this.props;
    const { currentPage } = this.state;
    const processed = this.getProcessedData();

    const startIndex = (currentPage - 1) * pageSize;
    return processed.slice(startIndex, startIndex + pageSize);
  }

  // Get total pages
  getTotalPages(): number {
    const { pageSize = 10 } = this.props;
    return Math.ceil(this.getProcessedData().length / pageSize);
  }

  // Handle column sort
  handleSort = (column: keyof T) => {
    this.setState(prevState => ({
      sortColumn: column,
      sortDirection:
        prevState.sortColumn === column && prevState.sortDirection === 'asc'
          ? 'desc'
          : 'asc',
      currentPage: 1,
    }));
  };

  // Handle page change
  handlePageChange = (page: number) => {
    this.setState({ currentPage: page });
  };

  // Handle row selection
  handleRowSelect = (index: number) => {
    const { onSelectionChange } = this.props;

    this.setState(prevState => {
      const newSelected = new Set(prevState.selectedRows);
      
      if (newSelected.has(index)) {
        newSelected.delete(index);
      } else {
        newSelected.add(index);
      }

      return { selectedRows: newSelected };
    }, () => {
      // Notify parent after state update
      if (onSelectionChange) {
        const pageData = this.getCurrentPageData();
        const selected = Array.from(this.state.selectedRows)
          .map(i => pageData[i])
          .filter(Boolean);
        onSelectionChange(selected);
      }
    });
  };

  // Handle select all
  handleSelectAll = () => {
    const { onSelectionChange } = this.props;
    const pageData = this.getCurrentPageData();

    this.setState(prevState => {
      const allSelected = prevState.selectedRows.size === pageData.length;
      const newSelected = allSelected
        ? new Set<number>()
        : new Set(pageData.map((_, i) => i));

      return { selectedRows: newSelected };
    }, () => {
      if (onSelectionChange) {
        const pageData = this.getCurrentPageData();
        const selected = Array.from(this.state.selectedRows)
          .map(i => pageData[i])
          .filter(Boolean);
        onSelectionChange(selected);
      }
    });
  };

  // Handle search with debounce
  handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;

    // Update input immediately for responsiveness
    this.setState({ searchTerm: value });

    // Debounce the actual filtering
    if (this.searchTimer) {
      clearTimeout(this.searchTimer);
    }

    this.searchTimer = setTimeout(() => {
      this.setState({ currentPage: 1 });
    }, 300);
  };

  // Handle row click
  handleRowClick = (row: T) => {
    const { onRowClick } = this.props;
    if (onRowClick) {
      onRowClick(row);
    }
  };

  render() {
    const { columns } = this.props;
    const { currentPage, sortColumn, sortDirection, selectedRows, searchTerm } =
      this.state;

    const pageData = this.getCurrentPageData();
    const totalPages = this.getTotalPages();
    const allSelected = selectedRows.size === pageData.length && pageData.length > 0;

    return (
      <div className="data-table">
        {/* Search */}
        <div className="table-controls">
          <input
            type="text"
            value={searchTerm}
            onChange={this.handleSearchChange}
            placeholder="Search..."
            className="table-search"
          />
        </div>

        {/* Table */}
        <table>
          <thead>
            <tr>
              <th>
                <input
                  type="checkbox"
                  checked={allSelected}
                  onChange={this.handleSelectAll}
                />
              </th>
              {columns.map(column => (
                <th
                  key={String(column.key)}
                  onClick={() =>
                    column.sortable && this.handleSort(column.key)
                  }
                  className={column.sortable ? 'sortable' : ''}
                >
                  {column.label}
                  {sortColumn === column.key && (
                    <span className="sort-indicator">
                      {sortDirection === 'asc' ? ' ↑' : ' ↓'}
                    </span>
                  )}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {pageData.map((row, index) => (
              <tr
                key={row.id}
                onClick={() => this.handleRowClick(row)}
                className={selectedRows.has(index) ? 'selected' : ''}
              >
                <td onClick={e => e.stopPropagation()}>
                  <input
                    type="checkbox"
                    checked={selectedRows.has(index)}
                    onChange={() => this.handleRowSelect(index)}
                  />
                </td>
                {columns.map(column => (
                  <td key={String(column.key)}>
                    {column.render
                      ? column.render(row[column.key], row)
                      : String(row[column.key])}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>

        {/* Pagination */}
        <div className="pagination">
          <button
            disabled={currentPage === 1}
            onClick={() => this.handlePageChange(currentPage - 1)}
          >
            Previous
          </button>
          <span>
            Page {currentPage} of {totalPages}
          </span>
          <button
            disabled={currentPage === totalPages}
            onClick={() => this.handlePageChange(currentPage + 1)}
          >
            Next
          </button>
        </div>

        {/* Selection info */}
        {selectedRows.size > 0 && (
          <div className="selection-info">
            {selectedRows.size} row(s) selected
          </div>
        )}
      </div>
    );
  }
}

export default DataTable;
export type { Column };
