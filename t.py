
class Triple(object):
    """ Captures a set of co-inputs, co-outputs and edges between two metagraph elements.
    """

    def __init__(self, coinputs, cooutputs, edges):
        if edges is None:
            raise MetagraphException('edges', resources['value_null'])

        if not (isinstance(coinputs, frozenset) or isinstance(coinputs, set) or coinputs is None):
            raise MetagraphException('coinputs', resources['format_invalid'])
        if not (isinstance(cooutputs, frozenset) or isinstance(cooutputs, set) or cooutputs is None):
            raise MetagraphException('cooutputs', resources['format_invalid'])

        if isinstance(coinputs, frozenset) or coinputs is None:
            self.coinputs = coinputs
        else:
            self.coinputs = frozenset(coinputs)

        if isinstance(cooutputs, frozenset) or cooutputs is None:
            self.cooutputs = cooutputs
        else:
            self.cooutputs = frozenset(cooutputs)

        if isinstance(edges, list):
            self.edges = edges
        else:
            self.edges = [edges]

    def coinputs(self):
        """ The co-inputs of the Triple object
        :return: set
        """
        return self.coinputs

    def cooutputs(self):
        """ The co-outputs of the Triple object
        :return: set
        """
        return self.cooutputs

    def edges(self):
        """ The edges of the Triple object
        :return: set
        """
        return self.edges

    def __repr__(self):
        if isinstance(self.edges, list):
            edge_desc = [repr(edge) for edge in self.edges]
        else:
            edge_desc = [repr(self.edges)]
        full_desc = ''
        for desc in edge_desc:
            if full_desc == '':
                full_desc = desc
            else:
                full_desc += ', ' + desc
        return 'Triple(%s, %s, %s)' % (self.coinputs, self.cooutputs, full_desc)

    def __eq__(self, other):
        if other is None:
            return False
        if not isinstance(other, Triple):
            return False

        return (self.coinputs == other.coinputs and
                self.cooutputs == other.cooutputs and
                len(self.edges) == len(other.edges) and
                self.edges == other.edges)

    def __lt__(self, other):
        s1 = str(self.coinputs) if self.coinputs is None else str(sorted(self.coinputs))
        s1 += str(self.cooutputs) if self.cooutputs is None else str(sorted(self.cooutputs))
        s1 += str(self.edges)
        s2 = str(other.coinputs) if other.coinputs is None else str(sorted(other.coinputs))
        s2 += str(other.cooutputs) if other.cooutputs is None else str(sorted(other.cooutputs))
        s2 += str(other.edges)
        return s1 < s2

    # coinputs and coutputs are frozensets so they can be hashed
    # sets cannot be hashed and using hash(str(someset)) is not robust
    # since the order of the elements in the returned string need
    # not be the same
    def __hash__(self):
        # Python tuples use a simplified version of the xxHash algorithm to capture order
        return hash((self.coinputs, self.coinputs)) ^ hash(tuple(self.edges))


class Edge(object):
    """ Represents a metagraph edge.
    """

    def __init__(self, invertex, outvertex, attributes=None, label=None):
        if invertex is None or len(invertex) == 0:
            raise MetagraphException('invertex', resources['value_null'])
        if outvertex is None or len(outvertex) == 0:
            raise MetagraphException('outvertex', resources['value_null'])
        if not isinstance(invertex, frozenset) and not isinstance(invertex, set):
            raise MetagraphException('invertex', resources['format_invalid'])
        if not isinstance(outvertex, frozenset) and not isinstance(outvertex, set):
            raise MetagraphException('outvertex', resources['format_invalid'])
        if label is not None and not isinstance(label, str):
            raise MetagraphException('outvertex', resources['format_invalid'])

        if isinstance(invertex, frozenset):
            self.invertex = invertex
        else:
            self.invertex = frozenset(invertex)

        if isinstance(outvertex, frozenset):
            self.outvertex = outvertex
        else:
            self.outvertex = frozenset(outvertex)

        self.attributes = attributes
        self.label = label

        # include attributes as part if invertex
        # this is why we dont need the attributes as part of the hash function
        if attributes is not None:
            invertex = list(self.invertex)
            for attribute in attributes:
                if attribute not in invertex:
                    invertex.append(attribute)
            self.invertex = frozenset(invertex)

    def __repr__(self):
        return 'Edge(%s, %s)' % (self.invertex, self.outvertex)

    def invertex(self):
        """ Returns the invertex of the edge.
        :return: set
        """
        return self.invertex

    def outvertex(self):
        """ Returns the outvertex of the edge.
        :return: set
        """
        return self.outvertex

    def label(self):
        """ Returns the label of the edge.
        :return: string
        """
        return self.label

    def __eq__(self, other):
        if other is None:
            return False
        if not isinstance(other, Edge):
            return False

        # TODO should equality check for equal labels too?
        return (self.invertex == other.invertex and
                self.outvertex == other.outvertex and
                self.attributes == other.attributes)

    # Invertex and Outvertex are frozensets so they can be hashed
    # sets cannot be hashed and using hash(str(someset)) is not robust
    # since the order of the elements in the returned string need
    # not be the same
    def __hash__(self):
        # Python tuples use a simplified version of the xxHash algorithm to capture order
        return hash(self.label) ^ hash((self.invertex, self.outvertex))


class Metapath(object):
    """ Represents a metapath between a source and a target node in a metagraph.
    """

    def __init__(self, source, target, edge_list):
        if source is None or len(source) == 0:
            raise MetagraphException('source', resources['value_null'])
        if target is None or len(target) == 0:
            raise MetagraphException('target', resources['value_null'])

        self.source = source
        self.target = target
        self.edge_list = edge_list

    def source(self):
        """ Returns the source of the metapath.
        :return: set
        """
        return self.source

    def target(self):
        """ Returns the target of the metapath.
        :return: set
        """
        return self.target

    def edge_list(self):
        """ Returns the list of edges of the metapath.
        :return: set
        """
        return self.edge_list

    def __repr__(self):
        edge_desc = [repr(edge) for edge in self.edge_list]
        full_desc = 'source: %s, target: %s' % (self.source, self.target)
        for desc in edge_desc:
            if full_desc == '':
                full_desc = desc
            else:
                full_desc += ", " + desc
        return 'Metapath({ %s })' % full_desc

    def dominates(self, metapath):
        """Checks whether current metapath dominates that provided.
        :param metapath: Metapath object
        :return: boolean
        """
        if metapath is None:
            raise MetagraphException('metapath', resources['value_null'])

        input1 = self.source  # B
        input2 = metapath.source  # B'

        output1 = self.target  # C
        output2 = metapath.target  # C'

        if input1.issubset(input2) and output2.issubset(output1):  # B <= B', C' <= C
            return True

        return False





a = set(A)
b = set(B)