import os


class Item:
    def __init__(self, bib_id=None, item_id=None, authors=None, title=None, publishers=None, series=None, pubyear=None, acquired=None, deleted=None, genres=None, subjects=None, last_borrowed=None):
        self.bib_id = bib_id
        self.item_id = item_id
        self.authors = authors
        self.title = title
        self.publishers = publishers
        self.series = series
        self.pubyear = pubyear
        self.acquired = acquired
        self.deleted = deleted
        self.last_borrowed = last_borrowed
        self.genres = genres
        self.subjects = subjects

        self.circulation_sequence = None
        self.feature_vectors = None
        self.comparison_sequence = None

    def get_feature(self, feature):
        return '#'.join(getattr(self, feature)).replace(' ', '_')

    def set_circulation_sequence(self, circulation_sequence):
        self.circulation_sequence = circulation_sequence

    def set_feature_vectors(self, feature_vectors):
        self.feature_vectors = feature_vectors

    def get_feature_string(self):
        features = self.authors + self.publishers + \
            self.genres + self.subjects + self.series
        features = '#'.join(features)
        features = features.replace(' ', '_')
        return features

    def get_feature_idxs(self, item):
        if self.feature_vectors != None:
            return np.where(self.feature_vectors != 0)[0].tolist()[:-1]

    def get_feature_count(self):
        feature_count = len(self.authors) + len(self.publishers) + \
            len(self.genres) + len(self.subjects) + len(self.series)
        return feature_count

    def get_feature_counts(self):
        feature_counts = {
            'authors': len(self.authors),
            'publishers': len(self.publishers),
            'genres': len(self.genres),
            'subjects': len(self.subjects),
            'series': len(self.series)
        }

        return feature_counts

    def filter_features(self, features):
        self.authors, self.publishers, self.genres, self.subjects, self.series = (
            [] for i in range(5))

        for f in features:
            if f in self.authors:
                self.authors.append(f)
            elif f in self.publishers:
                self.publishers.append(f)
            elif f in self.genres:
                self.genres.append(f)
            elif f in self.subjects:
                self.subjects.append(f)
            elif f in self.series:
                self.series.append(f)

        return self.get_feature_count()

    def __str__(self):
        item_str = '\n' + '*' * os.get_terminal_size()[0]
        item_str += f'\nBib id: {self.bib_id}'
        item_str += f'\nItem id: {self.item_id}'
        item_str += f'\nAuthor: {self.authors}'
        item_str += f'\nPublisher: {self.publishers}'
        item_str += f'\nTitle: {self.title}'
        item_str += f'\nSeries: {self.series}'
        item_str += f'\nPublication year: {self.pubyear}'
        item_str += f'\nAcquired: {self.acquired}'
        item_str += f'\nDeleted: {self.deleted}'
        item_str += f'\nGenres: {self.genres}'
        item_str += f'\nSubjects: {self.subjects}'

        if hasattr(self, 'circulation_sequence'):
            item_str += f'\nCirculation sequence length: {len(self.circulation_sequence)}'

        item_str += '\n' + '*' * os.get_terminal_size()[0]

        return item_str

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getitem__(self, key):
        return getattr(self, key)
