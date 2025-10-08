package org.playmetric.repository;

import org.playmetric.model.UIInteractionEvent;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface UIInteractionEventRepository extends MongoRepository<UIInteractionEvent, String> {}
