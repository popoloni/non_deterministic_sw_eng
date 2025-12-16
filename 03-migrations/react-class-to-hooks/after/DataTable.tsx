// @ts-nocheck
/**
 * DataTable - Functional Component with Hooks (After Migration)
 * 
 * 📖 Book Reference: Chapter 7, Pattern 12 - Migration as Learning
 * 
 * Key transformations:
 * - Complex state → multiple useState or useReducer
 * - Instance variables → useRef
 * - componentDidUpdate → useEffect with deps
 * - componentWillUnmount → useEffect cleanup
 * - shouldComponentUpdate → useMemo for computed values
 * - Callbacks → useCallback
 * 
 * NOTE: This is demonstration code. Run `npm install` to enable type checking.
 */

import React, {
  useState,
  useEffect,
  useCallback,
  useMemo,
  useRef,
} from 'react';

// Types (unchanged)
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

/**
 * DataTable Functional Component
 * 
 * Migration notes:
 * - useState for each state variable
 * - useRef for the debounce timer (instance variable)
 * - useMemo replaces getProcessedData and provides shouldComponentUpdate optimization
 * - useEffect for data changes and cleanup
 * - useCallback for all event handlers
 */
function DataTable<T extends { id: string | number }>({
  data,
  columns,
  pageSize = 10,
  onRowClick,
  onSelectionChange,
}: Props<T>) {
  // State - separate useState for each variable
  const [currentPage, setCurrentPage] = useState(1);
  const [sortColumn, setSortColumn] = useState<keyof T | null>(null);
  const [sortDirection, setSortDirection] = useState<'asc' | 'desc'>('asc');
  const [selectedRows, setSelectedRows] = useState<Set<number>>(new Set());
  const [searchTerm, setSearchTerm] = useState('');
  const [debouncedSearchTerm, setDebouncedSearchTerm] = useState('');

  // Ref for debounce timer - replaces instance variable
  const searchTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  // Reset pagination when data changes - replaces componentDidUpdate
  useEffect(() => {
    setCurrentPage(1);
    setSelectedRows(new Set());
  }, [data]);

  // Debounce search term
  useEffect(() => {
    if (searchTimerRef.current) {
      clearTimeout(searchTimerRef.current);
    }

    searchTimerRef.current = setTimeout(() => {
      setDebouncedSearchTerm(searchTerm);
      setCurrentPage(1);
    }, 300);

    // Cleanup - replaces componentWillUnmount
    return () => {
      if (searchTimerRef.current) {
        clearTimeout(searchTimerRef.current);
      }
    };
  }, [searchTerm]);

  // Processed data - useMemo provides optimization (replaces shouldComponentUpdate logic)
  const processedData = useMemo(() => {
    let processed = [...data];

    // Filter by search term (using debounced value)
    if (debouncedSearchTerm) {
      const term = debouncedSearchTerm.toLowerCase();
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
  }, [data, debouncedSearchTerm, sortColumn, sortDirection]);

  // Current page data - derived from processedData
  const pageData = useMemo(() => {
    const startIndex = (currentPage - 1) * pageSize;
    return processedData.slice(startIndex, startIndex + pageSize);
  }, [processedData, currentPage, pageSize]);

  // Total pages
  const totalPages = useMemo(() => {
    return Math.ceil(processedData.length / pageSize);
  }, [processedData.length, pageSize]);

  // Check if all selected
  const allSelected = useMemo(() => {
    return selectedRows.size === pageData.length && pageData.length > 0;
  }, [selectedRows.size, pageData.length]);

  // Handle column sort
  const handleSort = useCallback((column: keyof T) => {
    setSortColumn(prevColumn => {
      setSortDirection(prev =>
        prevColumn === column && prev === 'asc' ? 'desc' : 'asc'
      );
      return column;
    });
    setCurrentPage(1);
  }, []);

  // Handle page change
  const handlePageChange = useCallback((page: number) => {
    setCurrentPage(page);
  }, []);

  // Handle row selection
  const handleRowSelect = useCallback((index: number) => {
    setSelectedRows(prev => {
      const newSelected = new Set(prev);
      
      if (newSelected.has(index)) {
        newSelected.delete(index);
      } else {
        newSelected.add(index);
      }

      return newSelected;
    });
  }, []);

  // Notify parent of selection changes
  useEffect(() => {
    if (onSelectionChange) {
      const selected = Array.from(selectedRows)
        .map(i => pageData[i])
        .filter(Boolean);
      onSelectionChange(selected);
    }
  }, [selectedRows, pageData, onSelectionChange]);

  // Handle select all
  const handleSelectAll = useCallback(() => {
    setSelectedRows(prev => {
      const allCurrentlySelected = prev.size === pageData.length;
      return allCurrentlySelected
        ? new Set<number>()
        : new Set(pageData.map((_, i) => i));
    });
  }, [pageData]);

  // Handle search change
  const handleSearchChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(e.target.value);
  }, []);

  // Handle row click
  const handleRowClick = useCallback((row: T) => {
    if (onRowClick) {
      onRowClick(row);
    }
  }, [onRowClick]);

  return (
    <div className="data-table">
      {/* Search */}
      <div className="table-controls">
        <input
          type="text"
          value={searchTerm}
          onChange={handleSearchChange}
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
                onChange={handleSelectAll}
              />
            </th>
            {columns.map(column => (
              <th
                key={String(column.key)}
                onClick={() => column.sortable && handleSort(column.key)}
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
              onClick={() => handleRowClick(row)}
              className={selectedRows.has(index) ? 'selected' : ''}
            >
              <td onClick={e => e.stopPropagation()}>
                <input
                  type="checkbox"
                  checked={selectedRows.has(index)}
                  onChange={() => handleRowSelect(index)}
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
          onClick={() => handlePageChange(currentPage - 1)}
        >
          Previous
        </button>
        <span>
          Page {currentPage} of {totalPages}
        </span>
        <button
          disabled={currentPage === totalPages}
          onClick={() => handlePageChange(currentPage + 1)}
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

export default DataTable;
export type { Column };
