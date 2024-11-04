class Hash
  def deep_dup
    each_with_object({}) do |(key, value), result|
      result[key.dup] = value.is_a?(Hash) ? value.deep_dup : value.is_a?(Array) ? value.map(&:dup) : value
    end
  end
end

class Node
  attr_reader :left, :right, :down, :up, :grid_state, :x, :y, :path_success

  def initialize(grid_state, x, y)
    @grid_state = grid_state
    @x = x
    @y = y

    @left = get_new_node(x, y - 1)
    @right = get_new_node(x, y + 1)
    @up = get_new_node(x - 1, y)
    @down = get_new_node(x + 1, y)
  end

  def get_new_node(x, y)
    next_node = @grid_state[:'0'].select { |node| node == [x, y] }

    if @grid_state[:'0'].empty? && @grid_state[:'2'].include?([x, y])
      finish
      return nil
    elsif next_node.empty?
      return nil
    end

    new_state = @grid_state.deep_dup
    {
      x: x,
      y: y,
      grid_statement: update_statement!(new_state, next_node.first)
    }
  end

  def update_statement!(new_state, next_node)
    new_state[:'0'].delete(next_node)
    new_state[:'1'] << next_node unless new_state[:'1'].include?(next_node)
    new_state
  end

  def finish
    @path_success = true unless defined?(@path_success)
  end
end

class Grid
  NODES_STATEMENT = {
    '1': [],
    '0': [],
    '2': [],
    '-1': []
  }.freeze

  attr_reader :nodes_statement

  def initialize(grid)
    @grid = grid
    @nodes_statement = create_statement
  end

  def create_statement
    nodes_statement = NODES_STATEMENT.dup

    x = 0
    @grid.each do |elem|
      elem.each_with_index do |cell_value, y|
        nodes_statement[cell_value.to_s.to_sym] << [x, y]
      end
      x += 1
    end

    nodes_statement
  end
end

def unique_paths_iii(grid)
  grid_obj = Grid.new(grid)
  robot = grid_obj.nodes_statement[:'1'].first
  node = Node.new(grid_obj.nodes_statement.deep_dup, robot[0], robot[1])

  next_nodes = [node.left, node.right, node.down, node.up].compact

  next_nodes.any? ? parse_binary_tree_plus(next_nodes, 0) : 0
end

def parse_binary_tree_plus(nodes, paths_count)
  nodes.each do |node|
    new_node = Node.new(node[:grid_statement].deep_dup, node[:x], node[:y])

    next_nodes = [new_node.left, new_node.right, new_node.down, new_node.up].compact

    if new_node.path_success
      paths_count += 1
    elsif next_nodes.any?
      paths_count = parse_binary_tree_plus(next_nodes, paths_count)
    end
  end

  paths_count
end

puts unique_paths_iii(grid)
