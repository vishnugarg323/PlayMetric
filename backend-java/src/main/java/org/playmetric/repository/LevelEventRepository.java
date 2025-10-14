package org.playmetric.repository;

import org.playmetric.model.LevelEvent;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface LevelEventRepository extends MongoRepository<LevelEvent, String> {}
