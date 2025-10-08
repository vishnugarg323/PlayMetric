package org.playmetric.repository;

import org.playmetric.model.*;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface GameEventRepository extends MongoRepository<GameEvent, String> {}
